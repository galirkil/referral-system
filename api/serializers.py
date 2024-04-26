from django.urls import reverse
from rest_framework import serializers

from users.models import User
from users.validators import (LettersDigitsValidator, OnlyDigitsValidator,
                              PhoneValidator)


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[PhoneValidator()], max_length=16,
                                  required=True)


class AuthenticationCodeSerializer(PhoneSerializer):
    authentication_code = serializers.CharField(
        validators=[OnlyDigitsValidator()],
        max_length=4,
        required=True
    )


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(validators=[LettersDigitsValidator()],
                                        max_length=6, required=True)

    def validate_invite_code(self, value):
        user = self.context["request"].user

        if user.invited_by:
            raise serializers.ValidationError(
                "Инвайт-код можно активировать только один раз")

        if not User.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError("Недействительный инвайт-код")

        if user.invite_code == value:
            raise serializers.ValidationError(
                "Нельзя активировать свой инвайт-код")

        return value


class UserProfileSerializer(serializers.ModelSerializer):
    activate_invite_code = serializers.SerializerMethodField(read_only=True)
    invited_by_code = serializers.ReadOnlyField(
        source='invited_by.invite_code')
    invited_users = serializers.SerializerMethodField(read_only=True)

    def get_activate_invite_code(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('api:activate-invite-code'))

    def get_invited_users(self, obj):
        queryset = obj.invited_users.all()
        phones = queryset.values_list("phone", flat=True)
        return list(phones)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.invited_by:
            data.pop('activate_invite_code', None)
        else:
            data.pop('invited_by_code', None)
        return data

    class Meta:
        model = User
        fields = [
            'phone',
            'username',
            'email',
            'first_name',
            'last_name',
            'invite_code',
            'invited_by_code',
            'activate_invite_code',
            'invited_users'
        ]

        read_only_fields = ['invite_code']
