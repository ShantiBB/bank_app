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

User = get_user_model()

@shared_task(bind=True)
@transaction.atomic
def transaction_task(
        self,
        initiator_id,
        account_id,
        target_id,
        amount,
        transaction_type
):
    """Фоновая задача для обработки транзакции"""
    try:
        account = get_object_or_404(Account, id=account_id)
        initiator = get_object_or_404(User, id=initiator_id)
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
    except Exception as exp:
        self.retry(exp=exp, countdown=60)
