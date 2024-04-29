import time

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, views, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from api.permissions import IsOwnerOrAdmin
from api.serializers import (AuthenticationCodeSerializer,
                             InviteCodeSerializer, PhoneSerializer,
                             UserProfileSerializer)
from api.utils import generate_authentication_code
from users.models import User


class RequestAuthCodeView(views.APIView):
    """
    Принимает номер телефона в формате: '+123456789', отправляет код
    аутентификации на указанный номер.

    Приложение в тестовом режиме, код аутентификации будет возращен
    в теле ответа.
    """

    @extend_schema(
        summary="Отправить код аутентификации на номер телефона",
        request=PhoneSerializer,
        responses={200: PhoneSerializer},
        auth=[]
    )
    def post(self, request: Request) -> Response:
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            phone=serializer.validated_data["phone"])
        user.authentication_code = generate_authentication_code()
        user.save()

        #  Имитация отправки кода подтверждения по sms
        time.sleep(2)

        #  Пока нет отправки sms, отдаем код просто в ответе для тестирования
        temp_response = {
            "phone": user.phone,
            "authentication_code": user.authentication_code
        }
        return Response(temp_response, status=status.HTTP_200_OK)


class ObtainTokensView(views.APIView):
    """
    Принимает номер телефона и код аутентификации, возвращает пару
    access и refresh jwt-токенов для аутентификации на защищенных эндпоинтах.
    """

    @extend_schema(
        summary="Получить jwt-токены",
        request=AuthenticationCodeSerializer,
        responses={200: TokenObtainPairSerializer},
        auth=[],
    )
    def post(self, request: Request) -> Response:
        serializer = AuthenticationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authentication_code = serializer.validated_data["authentication_code"]
        phone = serializer.validated_data["phone"]
        user = get_object_or_404(User, phone=phone)
        if user.authentication_code != authentication_code:
            user.authentication_code = ''
            user.save()
            raise AuthenticationFailed("Введен неверный код аутентификации!")
        user.authentication_code = ''
        user.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        return Response(tokens, status=status.HTTP_200_OK)


class ActivateInviteCodeView(views.APIView):
    """
    Принимает инвайт-код код для активации. Код можно активировать один раз.
    Эндпоинт доступен из профиля пользователя, если ранее пользователь
    не активировал код.
    """
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Активировать инвайт-код",
        request=InviteCodeSerializer,
        responses={200: InviteCodeSerializer}
    )
    def post(self, request: Request) -> Response:
        user = request.user
        serializer = InviteCodeSerializer(data=request.data,
                                          context={"request": request})
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data["invite_code"]
        user.invited_by = User.objects.get(invite_code=invite_code)
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    retrieve=extend_schema(summary='Получить информацию о пользователе'),
    partial_update=extend_schema(summary='Обновить информацию о пользователе')
)
class UserRetrieveUpdateViewSet(mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    Возвращает/обновляет информацию о пользователе в зависимости от
    метода запроса.

    Если пользователь ранее активировал инвайт-код ответ будет содержать
    поле: invited_by_code, иначе поле - activate_invite_code со ссылкой
    на эндпойнт для активации инвайт-кода.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'phone'
    http_method_names = ["get", "patch"]


@extend_schema(summary="Обновить access-токен")
class CustomRefreshTokenView(TokenRefreshView):
    """
    Принимает refresh-токен и возращает access-токен, если refresh-токен
    действителен.
    """
    pass
