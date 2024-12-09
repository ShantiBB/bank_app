from django.contrib.auth import get_user_model
from django.db import models

from core.constants import ACCOUNT_TYPES, CURRENCY_CHOICES, STATUS_CHOICES


class Account(models.Model):
    title = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Название счета'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание счета'
    )
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма перевода'
    )
    account_type = models.CharField(
        max_length=10,
        default='checking',
        choices=ACCOUNT_TYPES,
        verbose_name='Тип счета'
    )
    currency = models.CharField(
        max_length=10,
        default='RUB',
        choices=CURRENCY_CHOICES,
        verbose_name='Валюта'
    )
    status_account = models.CharField(
        max_length=10,
        default='active',
        choices=STATUS_CHOICES,
        verbose_name='Статус счета'
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Владелец счета'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего обновления'
    )

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
        # ordering = ['-created_at']

    def __str__(self):
        return self.title
