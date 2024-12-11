from rest_framework import serializers

from services.tasks import transaction_task, transaction_task_status
from transactions.models import Transaction
from api.validators import validate_target_account, validate_balance


class TransactionListSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='account.currency', read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'id',
            'amount',
            'currency',
            'transaction_type',
            'account'
        )


class TransactionDetailSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source='account.currency', read_only=True)
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')
    status = serializers.SerializerMethodField(source='transaction')

    class Meta:
        model = Transaction
        fields = (
            'id',
            'status',
            'amount',
            'currency',
            'message',
            'transaction_type',
            'account',
            'created_at'
        )

    @staticmethod
    def get_status(obj):
        status = transaction_task_status(obj)

        if status == 'SUCCESS':
            return 'Выполнено'
        elif status == 'FATAL':
            return 'Ошибка при выполнении транзакции'
        else:
            return 'В обработке'


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
        initiator = self.context['request'].user
        account = validated_data.get('account')
        target_account_id = validated_data.get('target_account')
        amount = validated_data.get('amount')
        transaction_type = validated_data.get('transaction_type')

        task_transaction = transaction_task.apply_async(
            args= (
                initiator.id,
                account.id,
                target_account_id,
                amount,
                transaction_type,
            )
        )
        return validated_data
