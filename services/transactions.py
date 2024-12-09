from services.utils import convert_currency


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
