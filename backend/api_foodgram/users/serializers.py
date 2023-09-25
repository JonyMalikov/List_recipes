from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import User


class CustomUserSerializer(UserSerializer):
    """Serializer для пользователя."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        """Проверяет подписку на автора."""
        user = self.context["request"].user
        return (
            obj.following.filter(user=user).exists() and user.is_authenticated
        )

    def create(self, validated_data):
        """Создает и возвращает пользователя."""
        return User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        read_only_fields = fields


class UserFollowSerializer(CustomUserSerializer):
    """Serializer для подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        """Получает список рецептов автора."""
        request = self.context["request"]
        recipes = obj.recipes.values("id", "name", "image", "cooking_time")
        base_url = request.build_absolute_uri("/media/")
        for recipe in recipes:
            image_url = base_url + recipe["image"]
            recipe["image"] = image_url
        return recipes

    def get_recipes_count(self, obj):
        """Получает количество рецептов автора."""
        return obj.recipes.count()

    def validate_subscribe(self, attrs):
        """Проверяет подписку на автора."""
        user = self.context["request"].user
        following = self.instance

        if following.following.filter(user=user).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора"
            )
        return attrs

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = fields
