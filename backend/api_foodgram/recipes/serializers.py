from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api_foodgram.settings import (
    MAX_COOKING_TIME,
    MIN_COOKING_TIME,
)
from users.serializers import CustomUserSerializer
from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag,
)
from .validators import ingredients_validator, tags_validator


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]
        read_only_fields = ["id", "name", "image", "cooking_time"]


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]
        read_only_fields = ["id", "name", "color", "slug"]


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]
        read_only_fields = ["id", "name", "measurement_unit"]


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания новых рецептов."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME, max_value=MAX_COOKING_TIME
    )

    def get_is_favorited(self, obj):
        """Получает список избранных рецептов автора"""
        request = self.context["request"]
        if request.user.is_authenticated:
            return obj.recipe_favorites.filter(user=request.user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """Получает список покупок автора"""
        current_user = self.context["request"].user
        return obj.recipes_shopping_list.filter(user=current_user).exists()

    def get_ingredients(self, recipe):
        """Получает список ингредиентов рецепта"""

        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit"
        )
        return ingredients

    def validate(self, data):
        """Проверяет валидность данных"""
        request_method = self.context["request"].method
        tags = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")

        if request_method == "POST":
            tags = tags_validator(tags, Tag)
            ingredients = ingredients_validator(ingredients, Ingredient)

        data.update(
            {
                "tags": tags,
                "ingredients": ingredients,
                "author": self.context["request"].user,
            }
        )

        return data

    def create_ingredients(self, ingredients, recipe):
        """Создает ингредиенты"""
        ingredient_ids = [ing["id"] for ing in ingredients]
        recipe_ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
        recipe_ingredient_instances = [
            RecipeIngredient(
                ingredient=ingredient, recipe=recipe, amount=ing["amount"]
            )
            for ingredient, ing in zip(recipe_ingredients, ingredients)
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredient_instances)

    def create(self, validated_data):
        """Создает рецепт"""
        recipe_tags = validated_data.pop("tags")
        recipe_ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(recipe_tags)
        self.create_ingredients(recipe_ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Обновляет рецепт"""
        instance.name = validated_data.get("name", instance.name)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.text = validated_data.get("text", instance.text)
        instance.image = validated_data.get("image", instance.image)

        updated_tags = validated_data.get("tags")
        if isinstance(updated_tags, list):
            instance.tags.clear()
            instance.tags.set(updated_tags)

        updated_ingredients = validated_data.get("ingredients")
        if isinstance(updated_ingredients, list):
            instance.ingredients.clear()
            self.create_ingredients(updated_ingredients, instance)

        instance.save()
        return instance

    def validate_shopping_cart(self, recipe):
        """Проверяет валидность данных"""
        user = self.context["request"].user
        if user.user_shopping_lists.filter(recipe=recipe).exists():
            raise serializers.ValidationError("Рецепт уже в списке покупок")
        return recipe

    def validate_favorite(self, recipe):
        """Проверяет валидность данных"""
        user = self.context["request"].user
        if user.user_favorites.filter(recipe=recipe).exists():
            raise serializers.ValidationError("Рецепт уже в избранном")
        return recipe

    class Meta:
        model = Recipe
        fields = [
            "id",
            "author",
            "name",
            "image",
            "cooking_time",
            "text",
            "tags",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
        ]
        read_only_fields = [
            "author",
            "time_create",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        ]


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    class Meta:
        model = ShoppingList
        fields = ["id", "user", "recipe"]
        read_only_fields = ["user", "recipe"]


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов."""

    class Meta:
        model = Favorite
        fields = ["id", "user", "recipe"]
        read_only_fields = ["user", "recipe"]
