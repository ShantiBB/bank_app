from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

from api.serializers import TransactionCreateSerializer
from transactions.models import Transaction


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionCreateSerializer
    queryset = Transaction.objects.all()
    permission_classes = (CurrentUserOrAdmin,)
    http_method_names = ('get', 'post')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
