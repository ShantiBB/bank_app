from time import sleep

from django.db import transaction
from django.shortcuts import get_object_or_404
from celery import shared_task
from celery.result import AsyncResult
from celery.exceptions import MaxRetriesExceededError

from services.utils import delete_account_cache, delete_transaction_cache
from transactions.models import Account, Transaction
from services.transactions import (
    transaction_deposit,
    transaction_withdrawal,
    transaction_transfer,
)


@shared_task(
    bind=True,
    name='transaction_task',
    autoretry_for=(Exception,),
    default_retry_delay=5
)
def transaction_task(
        self,
        initiator_id,
        account_id,
        target_id,
        amount,
        transaction_type
):
    """Фоновая задача для обработки транзакции"""
    with transaction.atomic():
        queryset = Account.objects.select_related('owner')
        account = get_object_or_404(queryset, id=account_id)
        initiator = account.owner

        if transaction_type == 'deposit':
            transaction_deposit(account, amount)
        elif transaction_type == 'withdrawal':
            transaction_withdrawal(account, amount)
        elif transaction_type == 'transfer':
            target_account = get_object_or_404(Account, id=target_id)
            transaction_transfer(account, target_account, amount)

        task_id = self.request.id
        transaction_obj = Transaction.objects.create(
            initiator=initiator,
            account=account,
            amount=amount,
            transaction_type=transaction_type,
            status_id=task_id
        )
    sleep(10)  # Симуляция обработки транзакции

    if self.request.retries == 3:
        raise MaxRetriesExceededError()


def transaction_task_status(instance):
    """Получение статуса задачи по ID"""
    status = AsyncResult(instance.status_id)
    info = status.info

    if isinstance(info, MaxRetriesExceededError):
        return 'FATAL'
    return status.state
