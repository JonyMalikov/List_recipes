from django.core.exceptions import ValidationError

from api_foodgram.settings import MAX_AMOUNT, MIN_AMOUNT


def tags_validator(tags, tag):
    """Проверяет валидность тэгов."""
    if not tags:
        raise ValidationError("Не указаны тэги")
    if len(set(tags)) != len(tags):
        raise ValidationError("В запросе повторяющиеся тэги")
    if not tag.objects.filter(id__in=tags).count() == len(tags):
        raise ValidationError("В запросе несуществующий тэг")
    return tags


def ingredients_validator(ingredients, ingredient):
    """Проверяет валидность ингредиентов."""
    validation_errors = []

    if not ingredients:
        validation_errors.append("Не указаны ингредиенты")

    ingredient_ids = {ing["id"] for ing in ingredients}
    ingredients_obj = ingredient.objects.filter(id__in=ingredient_ids)

    if len(ingredient_ids) != len(ingredients):
        validation_errors.append("В запросе повторяющиеся ингредиенты")

    if len(ingredients_obj) != len(ingredient_ids):
        validation_errors.append("В запросе несуществующие ингредиенты")

    for ing in ingredients:
        if "amount" in ing and (
            int(ing["amount"]) < MIN_AMOUNT or int(ing["amount"]) > MAX_AMOUNT
        ):
            validation_errors.append(
                "Некорректное значение количества ингредиента"
            )

    if validation_errors:
        raise ValidationError(", ".join(validation_errors))

    return ingredients
