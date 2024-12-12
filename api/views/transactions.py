from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from transactions.models import Transaction
from api.serializers import (
    TransactionListSerializer,
    TransactionCreateSerializer,
    TransactionDetailSerializer
)
from services.utils import check_response_cache, delete_transaction_cache


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionCreateSerializer
    permission_classes = (CurrentUserOrAdmin,)
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self):
        if self.action == 'list':
            return TransactionListSerializer
        elif self.action == 'retrieve':
            return TransactionDetailSerializer
        return TransactionCreateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(initiator=user)
        return queryset.select_related('account')

    def list(self, request, *args, **kwargs):
        cache_key = f'transaction_list_{self.request.user.id}'
        return check_response_cache(self, request, cache_key, *args, **kwargs)
