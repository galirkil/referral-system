from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone",)
    readonly_fields = ("invited_users", "invite_code")

    def invited_users(self, obj):
        user_link_list = [self.user_link(user) for user in
                          obj.invited_users.all()]
        return format_html(", ".join(user_link_list))

    def user_link(self, user):
        url = reverse("admin:users_user_change", args=(user.id,))
        return f'<a href="{url}">{user.phone}</a>'

    invited_users.short_description = "Приглашенные пользователи"
