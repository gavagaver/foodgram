from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]