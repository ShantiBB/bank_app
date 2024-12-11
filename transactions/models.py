from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Account
from core.constants import TRANSACTION_TYPES


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма перевода'
    )
    message = models.TextField(
        null=True, blank=True,
        verbose_name='Сообщение'
    )
    status_id = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='Статус транзакции'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        verbose_name='Тип транзакции',
        default='transfer_in',
    )
    account = models.ForeignKey(
        Account,
        related_name='transactions',
        on_delete=models.CASCADE,
        verbose_name='Счет'
    )
    initiator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Инициатор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']

    def __str__(self):
        return (
            f'{self.amount} {self.account.currency} '
            f'на счет "{self.account.title}"'
        )
