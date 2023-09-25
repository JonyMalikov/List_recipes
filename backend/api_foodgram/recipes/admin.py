from django.contrib import admin

from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientinRecipeInLine(admin.TabularInline):
    """Модель связи ингредиента и рецепта"""

    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Модель тега"""

    prepopulated_fields = {"slug": ("name",)}
    list_display = ("id", "name", "color", "slug")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель рецепта"""

    inlines = (IngredientinRecipeInLine,)
    list_display = ("id", "name", "author", "time_create")
    list_filter = ("author", "name", "tags", "time_create")
    list_display_links = ("id", "name")
    search_fields = ("name", "text")


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    """Модель ингредиента"""

    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


@admin.register(RecipeIngredient)
class RecipeIngredientListAdmin(admin.ModelAdmin):
    """Модель связи рецепта и ингредиента"""

    list_display = ("recipe", "ingredient", "amount")
    list_filter = ("recipe",)


@admin.register(Favorite)
class FavoriteListAdmin(admin.ModelAdmin):
    """Модель избранных рецептов"""

    list_display = ("user", "recipe")
    list_filter = ("user",)
