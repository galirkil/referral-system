import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.validators import (LettersDigitsValidator, OnlyDigitsValidator,
                              PhoneValidator)


class User(AbstractUser):
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
        validators=[PhoneValidator()],
        max_length=16,
        unique=True
    )
    authentication_code = models.CharField(
        "код аутентификации",
        validators=[OnlyDigitsValidator()],
        max_length=4,
        blank=True
    )
    invite_code = models.CharField(
        "инвайт-код",
        validators=[LettersDigitsValidator],
        max_length=6,
        editable=False,
        blank=True
    )
    invited_by = models.ForeignKey(
        "self",
        related_name="invited_users",
        verbose_name="пользователь приглашен",
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
