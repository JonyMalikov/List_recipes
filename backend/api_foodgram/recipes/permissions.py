from rest_framework import permissions


class AdminOrReadOnlyPermission(permissions.BasePermission):
    """Права доступа администратора."""

    def new_function_name(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_superuser
        )


class AuthorOrReadOnlyPermission(permissions.BasePermission):
    """Права доступа автора."""

    def check_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_superuser
        )

    def check_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )
