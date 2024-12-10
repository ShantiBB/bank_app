from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from services.utils import delete_account_cache
from accounts.models import Account
from api.serializers import (
    AccountListSerializer,
    AccountDetailSerializer,
    AccountCreateSerializer
)


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
        cached_account = cache.get(cache_key)

        if cached_account:
            return Response(cached_account, status=status.HTTP_200_OK)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=3000)
        return response

    def retrieve(self, request, *args, **kwargs):
        account_id = kwargs.get('pk')
        cache_key = f'account_{account_id}'
        cached_account = cache.get(cache_key)

        if cached_account:
            return Response(cached_account, status=status.HTTP_200_OK)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=3000)
        return response


    def perform_create(self, serializer):
        account = serializer.save(owner=self.request.user)
        delete_account_cache(account, self.request.user)

    def perform_update(self, serializer):
        account = serializer.save()
        delete_account_cache(account, self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        delete_account_cache(instance, self.request.user)
