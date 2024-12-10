from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from celery import shared_task

from transactions.models import Account, Transaction
from services.transactions import (
    transaction_deposit,
    transaction_withdrawal,
    transaction_transfer,
)
from user.models import CustomUser

User = get_user_model()

@shared_task(
    name='transaction_task',
    autoretry_for=(Exception,),
    default_retry_delay=30
)
@transaction.atomic
def transaction_task(
        initiator_id,
        account_id,
        target_id,
        amount,
        transaction_type
):
    """Фоновая задача для обработки транзакции"""
    account = get_object_or_404(
        Account.objects.select_related('owner'),
        id=account_id,
    )
    initiator = account.owner
    if transaction_type == 'deposit':
        transaction_deposit(account, amount)
    elif transaction_type == 'withdrawal':
        transaction_withdrawal(account, amount)
    elif transaction_type == 'transfer':
        target_account = get_object_or_404(Account, id=target_id)
        transaction_transfer(account, target_account, amount)

    Transaction.objects.create(
        initiator=initiator,
        account=account,
        amount=amount,
        transaction_type=transaction_type,
    )
