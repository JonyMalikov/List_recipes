from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_foodgram.settings import (
    MAX_AMOUNT,
    MAX_COOKING_TIME,
    MIN_AMOUNT,
    MIN_COOKING_TIME,
)
from users.models import User


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="Цвет",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ярлык"
        verbose_name_plural = "Ярлыки"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единицы измерения",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Название",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Ярлык",
    )
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингредиенты в рецепте",
    )

    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_COOKING_TIME),
            MaxValueValidator(MAX_COOKING_TIME),
        ],
        verbose_name="Время приготовления",
    )
    image = models.ImageField(
        upload_to="recipe_images/%Y/%m/%d/",
        verbose_name="Картинка",
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Время создания",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель связи рецепта и ингредиента"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Cвязанные рецепты",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_recipes",
        verbose_name="Связанные ингредиенты",
    )

    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT),
        ],
        verbose_name="Количество ингредиента",
    )

    class Meta:
        ordering = ["recipe"]
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "recipe",
                    "ingredient",
                ),
                name="unique_ingredient",
            ),
        ]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return "{} {}".format(self.ingredient, self.amount)


class Favorite(models.Model):
    """Модель избранных рецептов"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_favorites",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_favorites",
        verbose_name="Избранный рецепт",
    )

    class Meta:
        verbose_name = "Избранный"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite"
            )
        ]

    def __str__(self):
        return "{} -> {}".format(self.user, self.recipe)


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_shopping_lists",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipes_shopping_list",
        verbose_name="Список покупок",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping"
            )
        ]

    def __str__(self):
        return "{} -> {}".format(self.user, self.recipe)
