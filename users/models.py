import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone_validator = RegexValidator(
        regex=r'^\+\d{10,15}$',
        message="Введите номер телефона до 15 цифр в формате: '+1234567890"
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone = models.CharField(
        "номер телефона",
        validators=[phone_validator],
        max_length=16,
        unique=True
    )
    authorization_code = models.CharField(
        "код авторизации",
        max_length=4,
        blank=True
    )
    invite_code = models.CharField(
        "инвайт-код",
        max_length=6,
        editable=False,
        blank=True
    )
    invited_by = models.ForeignKey(
        "self",
        related_name="invited_users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.phone

    def generate_invite_code(self, length=6) -> None:
        chars = string.digits + string.ascii_letters
        self.invite_code = ''.join(
            secrets.choice(chars) for _ in range(length))

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.generate_invite_code()
        super().save(*args, **kwargs)
