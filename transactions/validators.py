from rest_framework import serializers


def validate_target_account(account, target_account):
    """
    Проверка наличия счета для перевода и проверка на совпадение счетов.
    """
    if not target_account:
        raise serializers.ValidationError(
            'Не указан получатель перевода.'
        )
    if account == target_account:
        raise serializers.ValidationError(
            'Перевод на текущий счет невозможен.'
        )


def validate_balance(account, amount):
    """
    Проверка средств на счете для вывода или перевода.
    """
    dif_balance = account.balance - amount
    if dif_balance < 0:
        raise serializers.ValidationError(
            'Недостаточно средств на счету.'
        )
