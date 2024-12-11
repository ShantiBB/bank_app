from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import AccountViewSet
from api.views import TransactionViewSet

router = DefaultRouter()
router.register(
    r'accounts',
    AccountViewSet,
    basename='accounts'
)
router.register(
    r'transactions',
    TransactionViewSet,
    basename='transactions'
)

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
] + router.urls
