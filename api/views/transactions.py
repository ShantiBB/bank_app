from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from transactions.models import Transaction
from api.serializers import (
    TransactionListSerializer,
    TransactionCreateSerializer,
    TransactionDetailSerializer
)
from services.utils import check_response_cache


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionCreateSerializer
    permission_classes = (CurrentUserOrAdmin,)
    http_method_names = ('get', 'post', 'delete')

    def get_queryset(self):
        user = self.request.user
        values = (
            'id',
            'amount',
            'transaction_type',
            'account__title',
            'account__currency'
        )
        queryset = Transaction.objects.filter(initiator=user)

        if self.action == 'list':
            queryset = queryset.values(*values)
        elif self.action == 'retrieve':
            queryset = queryset.values(
                *values, 'message', 'created_at', 'status_id'
            )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TransactionListSerializer
        elif self.action == 'retrieve':
            return TransactionDetailSerializer
        return TransactionCreateSerializer

    def list(self, request, *args, **kwargs):
        cache_key = f'transaction_list_{self.request.user.id}'
        return check_response_cache(self, request, cache_key, *args, **kwargs)
