from django.core.cache import cache


def convert_currency(amount, from_currency, to_currency, exchange_rate=100):
    """
    Функция для конвертации валют USD и RUB.
    """
    if from_currency == 'USD' and to_currency == 'RUB':
        return amount * exchange_rate
    elif from_currency == 'RUB' and to_currency == 'USD':
        return amount / exchange_rate
    return amount


def delete_account_cache(instance, user):
    """Удаляет кэш после создания, обновления и удаления счета"""
    cache.delete(f'account_list_{user.id}')
    cache.delete(f'account_{instance.id}')
