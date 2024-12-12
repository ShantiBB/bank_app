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
        currency = obj.get('currency')
        balance = obj.get('balance')

        if currency == 'RUB':
            return f'{balance}р'
        elif currency == 'USD':
            return f'${balance}'


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
            'created_at'
        )


class AccountCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            'title',
            'description',
            'currency',
            'account_type'
        )


class AccountShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'currency')
