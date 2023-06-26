from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from recipes.models import Recipe

from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(
        method_name='get_is_subscribed',
    )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        return (
            not user.is_anonymous
            and user.subscribers.filter(author=obj).exists()
        )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(CustomUserSerializer):
    recipes = SerializerMethodField(
        method_name='get_recipes',
    )
    recipes_count = SerializerMethodField(
        method_name='get_recipes_count',
    )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = int(request.query_params.get('recipes_limit'))
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:limit]
        serializer = RecipeSubscribeSerializer(
            recipes,
            many=True,
            read_only=True,
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'username',
        )
