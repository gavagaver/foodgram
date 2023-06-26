from django.conf import settings as s
from django.contrib import admin
from .models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'username',
        'email',
    )
    empty_value_display = s.EMPTY_VALUE_DISPLAY


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    empty_value_display = s.EMPTY_VALUE_DISPLAY


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)

