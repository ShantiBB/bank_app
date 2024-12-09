from rest_framework import serializers


def validate_target_account(data):
    """
    Проверка наличия счета для перевода и проверка на совпадение счетов.
    """
    account = data.get('account')
    target_account = data.get('target_account')
    if not target_account:
        raise serializers.ValidationError(
            'Не указан получатель перевода.'
        )
    if account == target_account:
        raise serializers.ValidationError(
            'Перевод на текущий счет невозможен.'
        )


def validate_balance(data):
    """
    Проверка средств на счете для вывода или перевода.
    """
    account = data.get('account')
    amount = data.get('amount')
    dif_balance = account.balance - amount

    if dif_balance < 0:
        raise serializers.ValidationError(
            'Недостаточно средств на счету.'
        )
