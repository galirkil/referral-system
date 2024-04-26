from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Проверка прав доступа: только владелец или суперпользователь
    имеют доступ к объекту.
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_superuser
