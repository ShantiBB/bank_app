from django.db import transaction
from rest_framework import serializers

from accounts.models import Account
from core.constants import CURRENCY_CHOICES
from transactions.models import Transaction
from transactions.services import process_transaction
from transactions.validators import validate_target_account, validate_balance


class TransactionCreateSerializer(serializers.ModelSerializer):
    target_account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.filter(status_account='active'),
        write_only=True,
        allow_null=True,
    )
    currency = serializers.ChoiceField(
        source='account.currency',
        choices=CURRENCY_CHOICES,
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            'amount',
            'currency',
            'message',
            'transaction_type',
            'account',
            'target_account'
        )

    def validate(self, attrs):
        account = attrs.get('account')
        target_account = attrs.get('target_account')
        amount = attrs.get('amount')
        transaction_type = attrs.get('transaction_type')

        if transaction_type == 'transfer':
            validate_target_account(account, target_account)
        if transaction_type in ('transfer', 'withdrawal'):
            validate_balance(account, amount)
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            return process_transaction(validated_data)
