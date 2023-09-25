from django.contrib import admin

from .models import User, UserFollow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи"""

    list_display = ("id", "email", "first_name", "last_name")
    list_filter = (
        "first_name",
        "email",
    )
    list_display_links = ("id", "email", "first_name", "last_name")
    search_fields = (
        "first_name",
        "email",
    )


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    """Подписки"""

    list_display = ("user", "following")
    list_display_links = ("user", "following")
    list_filter = (
        "user",
        "following",
    )
    search_fields = ("user", "following")
