from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag,
)
from recipes.paginations import CustomPagination
from recipes.permissions import (
    AdminOrReadOnlyPermission,
    AuthorOrReadOnlyPermission,
)
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipesSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnlyPermission,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для работы с рецептами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (AuthorOrReadOnlyPermission,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(methods=["post", "delete"], detail=True)
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)

        serializer = RecipesSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        if request.method == "POST":
            shopping = ShoppingList.objects.create(user=user, recipe=recipe)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )

        shopping = get_object_or_404(ShoppingList, user=user, recipe=recipe)
        shopping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, pk):
        """Добавление рецепта в избранное."""
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = RecipesSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        user = self.request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__recipes_shopping_list__user=user
        ).values("ingredient__name", "ingredient__measurement_unit", "amount")
        ingredients_data = {}
        for ing in ingredients:
            name_unit = (
                f"{ing['ingredient__name']} "
                f"({ing['ingredient__measurement_unit']})"
            )
            amount = ing["amount"]
            ingredients_data[name_unit] = (
                ingredients_data.get(name_unit, 0) + amount
            )
        ingredient_list = "\n".join(
            [
                f"{name} -> {amount}"
                for name, amount in ingredients_data.items()
            ]
        )
        file = "shopping-list.txt"
        response = HttpResponse(ingredient_list, content_type="text/plain")
        response["Content-Disposition"] = f'attachment; filename="{file}.txt"'
        return response
