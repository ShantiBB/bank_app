from transactions.models import Transaction
from transactions.utils import convert_currency


def process_transaction(validated_data):
    """Обработка каждой транзакции"""

    account = validated_data.get('account')
    target_account = validated_data.get('target_account')
    amount = validated_data.get('amount')
    transaction_type = validated_data.get('transaction_type')

    if transaction_type == 'deposit':
        transaction_deposit(account, amount)
    elif transaction_type == 'withdrawal':
        transaction_withdrawal(account, amount)
    elif transaction_type == 'transfer':
        transaction_transfer(account, target_account, amount)

    initiator = validated_data.pop('owner')
    validated_data.pop('target_account')
    return Transaction.objects.create(
        initiator=initiator,
        **validated_data
    )


def transaction_deposit(account, amount):
    """Пополнение счета"""
    account.balance += amount
    account.save()


def transaction_withdrawal(account, amount):
    """Вывод со счета"""
    account.balance -= amount
    account.save()


def transaction_transfer(account, target_account, amount):
    """Перевод с одного счета на другой"""
    from_currency = account.currency
    to_currency = target_account.currency
    amount_convert = convert_currency(amount, from_currency, to_currency)

    account.balance -= amount
    account.save()
    target_account.balance += amount_convert
    target_account.save()
