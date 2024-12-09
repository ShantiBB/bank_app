from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from api.serializers import TransactionCreateSerializer
from transactions.models import Transaction


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionCreateSerializer
    permission_classes = (CurrentUserOrAdmin,)
    http_method_names = ('get', 'post')

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(initiator=user).select_related('account')
        return queryset
