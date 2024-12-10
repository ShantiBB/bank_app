from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from services.utils import delete_account_cache, check_cache, \
    delete_transaction_cache
from accounts.models import Account
from api.serializers import (
    AccountListSerializer,
    AccountDetailSerializer,
    AccountCreateSerializer
)
from core.django_config.settings import CACHE_TIMEOUT


class AccountViewSet(ModelViewSet):
    permission_classes = (CurrentUserOrAdmin,)
    http_method_names = ('get', 'post', 'put', 'delete')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountListSerializer
        elif self.action == 'retrieve':
            return AccountDetailSerializer
        return AccountCreateSerializer

    def list(self, request, *args, **kwargs):
        cache_key = f'account_list_{request.user.id}'
        return check_cache(self, request, cache_key, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        account_id = kwargs.get('pk')
        cache_key = f'account_{account_id}'
        return check_cache(self, request, cache_key, *args, **kwargs)

    def perform_create(self, serializer):
        account = serializer.save(owner=self.request.user)
        delete_account_cache(account.id, self.request.user.id)

    def perform_update(self, serializer):
        account = serializer.save()
        delete_account_cache(account.id, self.request.user.id)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        delete_account_cache(instance.id, self.request.user.id)
        # Для удаления связных транзакций из кэша
        delete_transaction_cache(None, self.request.user.id)
