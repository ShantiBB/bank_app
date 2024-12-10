from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from core.django_config.settings import CACHE_TIMEOUT


def convert_currency(amount, from_currency, to_currency, exchange_rate=100):
    """
    Функция для конвертации валют USD и RUB.
    """
    if from_currency == 'USD' and to_currency == 'RUB':
        return amount * exchange_rate
    elif from_currency == 'RUB' and to_currency == 'USD':
        return amount / exchange_rate
    return amount


def response_action_method(request, instance, *args, **kwargs):
    """
    Возвращает response наследованный от класса для списка и объекта.
    """
    class_calc = (type(instance), instance)
    if instance.action == 'list':
        return super(*class_calc).list(request, *args, **kwargs)
    return super(*class_calc).retrieve(request, *args, **kwargs)


def check_cache(instance, request, cache_key, *args, **kwargs):
    cached_object = cache.get(cache_key)
    if cached_object:
        return Response(cached_object, status=status.HTTP_200_OK)
    response = response_action_method(request, instance, *args, **kwargs)
    cache.set(cache_key, response.data, timeout=CACHE_TIMEOUT)
    return response


def delete_account_cache(instance_id, user_id):
    """Удаляет кэш после создания, обновления и удаления счета"""
    cache.delete(f'account_list_{user_id}')
    cache.delete(f'account_{instance_id}')


def delete_transaction_cache(instance_id, user_id):
    """Удаляет кэш после создания и удаления транзакции"""
    cache.delete(f'transaction_list_{user_id}')
    cache.delete(f'transaction_{instance_id}')
