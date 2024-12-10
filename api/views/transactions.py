from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from api.serializers import TransactionCreateSerializer
from transactions.models import Transaction
from services.utils import delete_account_cache


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionCreateSerializer
    permission_classes = (CurrentUserOrAdmin,)
    http_method_names = ('get', 'post')

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(initiator=user)
        return queryset.select_related('account')

    def perform_create(self, serializer):
        transaction = serializer.save(initiator=self.request.user)
        account = transaction.get('account')
        delete_account_cache(account, self.request.user)
