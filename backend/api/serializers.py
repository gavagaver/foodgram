from django.conf import settings as s
from django.core.validators import MinValueValidator
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from recipes.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    Favorite,
    ShoppingCart,
)
from users.serializers import CustomUserSerializer


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeIngredientReadSerializer(ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                s.MIN_INGREDIENT_AMOUNT,
                message=f'Минимальное количество: {s.MIN_INGREDIENT_AMOUNT}',
            ),
        ),
    )

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'amount',
        )


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        source='recipeingredient_set',
        many=True,
    )
    image = Base64ImageField()
    is_favorited = SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    def is_user_is_owner(self, request, obj, model):
        user = request.user
        return (
            user.is_authenticated
            and model.objects.filter(user=user, recipe=obj, ).exists()
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return self.is_user_is_owner(request, obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return self.is_user_is_owner(request, obj, ShoppingCart)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class RecipeWriteSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientWriteSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                s.MIN_COOKING_TIME,
                message=f'Минимальное время: {s.MIN_COOKING_TIME}',
            ),
        ),
    )

    def create_amount(self, recipe, ingredients):
        recipe_ingredients = []
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            recipe_ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=Ingredient(
                        pk=ingredient['id'],
                    ),
                    amount=amount,
                )
            )
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_amount(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags:
            instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients', None)
        if ingredients:
            instance.ingredients.clear()
            self.create_amount(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data

    def validate(self, data):
        ingredients = data.get('ingredients')

        id_list = [ingredient['id'] for ingredient in ingredients]
        if len(set(id_list)) != len(id_list):
            raise serializers.ValidationError(
                'Ингредиенты должны быть уникальными',
            )

        return data

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class RecipeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
