from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientLoginViewSet, ClientUserContextView

router = DefaultRouter()
router.register(r'client-logins', ClientLoginViewSet, basename='client-login')

urlpatterns = [
    path('client-logins/permissions-list/', ClientLoginViewSet.as_view({'get': 'list_permissions'}), name='client-login-permissions'),
    path('', include(router.urls)),
    path('client-user-context/', ClientUserContextView.as_view(), name='client-user-context'),
]
