from rest_framework.viewsets import ModelViewSet
from djoser.permissions import CurrentUserOrAdmin

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
