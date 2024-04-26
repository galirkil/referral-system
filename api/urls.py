from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from api.views import (ActivateInviteCodeView, ObtainTokensView,
                       RequestAuthCodeView, UserRetrieveUpdateViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserRetrieveUpdateViewSet, basename='user')

urlpatterns = [
    path('request-auth-code/', RequestAuthCodeView.as_view(),
         name='request-auth-code'),
    path('authenticate/', ObtainTokensView.as_view(), name='authenticate'),
    path('', include(router.urls)),
    path('users/activate-invite-code/', ActivateInviteCodeView.as_view(),
         name='activate-invite-code'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='api:schema'),
         name='redoc')
]
