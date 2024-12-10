from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from api.serializers import TransactionCreateSerializer
from transactions.models import Transaction
from services.utils import (
    delete_account_cache,
    check_cache,
    delete_transaction_cache
)


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionCreateSerializer
    permission_classes = (CurrentUserOrAdmin,)
    http_method_names = ('get', 'post', 'delete')

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(initiator=user)
        return queryset.select_related('account')

    def list(self, request, *args, **kwargs):
        cache_key = f'transaction_list_{self.request.user.id}'
        return check_cache(self, request, cache_key, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        transaction_id = kwargs.get('pk')
        cache_key = f'transaction_{transaction_id}'
        return check_cache(self, request, cache_key, *args, **kwargs)

    def perform_create(self, serializer):
        transaction = serializer.save(initiator=self.request.user)
        account = transaction.get('account')
        delete_account_cache(account.id, self.request.user.id)
        delete_transaction_cache(transaction.get('id'), self.request.user.id)

    def perform_destroy(self, instance):
        delete_transaction_cache(instance.id, self.request.user.id)
        super().perform_destroy(instance)
