from rest_framework import serializers

from services.tasks import transaction_task
from transactions.models import Transaction
from api.validators import validate_target_account, validate_balance


class TransactionCreateSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='account.currency', read_only=True)
    target_account = serializers.IntegerField(write_only=True, required=False)

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
        transaction_type = attrs.get('transaction_type')
        if transaction_type == 'transfer':
            validate_target_account(attrs)
        if transaction_type in ('transfer', 'withdrawal'):
            validate_balance(attrs)
        return attrs

    def create(self, validated_data):
        account = validated_data.get('account')
        amount = validated_data.get('amount')
        transaction_type = validated_data.get('transaction_type')
        initiator = self.context['request'].user
        target_account_id = validated_data.get('target_account')

        transaction_task.delay_on_commit(
            initiator_id=initiator.id,
            account_id=account.id,
            target_id=target_account_id,
            amount=amount,
            transaction_type=transaction_type,
        )
        return validated_data
