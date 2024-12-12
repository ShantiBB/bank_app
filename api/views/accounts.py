from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from accounts.models import Account
from services.utils import (
    delete_account_cache,
    check_response_cache,
    delete_transaction_cache
)
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
        return check_response_cache(self, request, cache_key, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        account_id = kwargs.get('pk')
        cache_key = f'account_{account_id}'
        return check_response_cache(self, request, cache_key, *args, **kwargs)

    def perform_create(self, serializer):
        account = serializer.save(owner=self.request.user)
