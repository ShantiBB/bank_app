from rest_framework import serializers

from accounts.models import Account


class AccountListSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            'id',
            'title',
            'balance',
            'account_type',
        )

    @staticmethod
    def get_balance(obj):
        if obj.currency == 'RUB':
            return f'{obj.balance}р'
        elif obj.currency == 'USD':
            return f'${obj.balance}'


class AccountDetailSerializer(AccountListSerializer):
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = Account
        fields = (
            'id',
            'title',
            'description',
            'balance',
            'account_type',
            'status_account',
            'created_at'
        )


class AccountCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            'title',
            'description',
            'balance',
            'account_type',
            'currency'
        )
        extra_kwargs = {
            'balance': {'read_only': True},
        }
