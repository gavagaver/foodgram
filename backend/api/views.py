from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from foodgram.pagination import CustomPagination
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeCardSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          TagSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        url_path='favorite',
        methods=('POST', 'DELETE'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'DELETE':
            Favorite.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = RecipeCardSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=('POST', 'DELETE'),
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeCardSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        methods=('GET',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        total_amounts = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user
        )
        for ingredient in ingredients:
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            ingredient_label = (
                f'{name} ({measurement_unit})'
            )
            ingredient_amount = ingredient.amount
            total_amounts[ingredient_label] = (
                total_amounts.get(ingredient_label, 0)
                + ingredient_amount
            )

        list_of_ingredients = []
        for ingredient_label, amount in total_amounts.items():
            list_of_ingredients.append(
                f'{ingredient_label} - {amount}'
            )

        header = 'Ваш список покупок\n' + '-------------------\n'
        footer = '-------------------\n' + 'Составлено в foodgram'
        response = HttpResponse(
            header + '\n' + '\n'.join(list_of_ingredients) + '\n' + footer,
            content_type='text/plain',
        )
        response['Content-Disposition'] = (
            'attachment; filename=Shopping_Cart.txt'
        )
        return response
