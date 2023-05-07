from django.conf import settings as s
from django.contrib import admin

from .models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingCart,
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    ordering = (
        'id',
    )
    empty_value_display = s.EMPTY_VALUE_DISPLAY


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
        'color',
        'slug',
    )
    ordering = (
        'name',
    )
    empty_value_display = s.EMPTY_VALUE_DISPLAY


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'favorites',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    ordering = (
        'name',
    )
    empty_value_display = s.EMPTY_VALUE_DISPLAY

    def favorites(self, obj):
        return obj.favorites.count()


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    empty_value_display = s.EMPTY_VALUE_DISPLAY


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    empty_value_display = s.EMPTY_VALUE_DISPLAY


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
