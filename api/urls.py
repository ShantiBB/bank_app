from django.urls import path, include

urlpatterns = [
    path('', include('djoser.urls')),
    path(r'', include('djoser.urls.authtoken')),
]
