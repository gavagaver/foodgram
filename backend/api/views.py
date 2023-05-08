from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Tag

from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter
from .permissions import IsAdminOrReadOnly
from .serializers import IngredientSerializer, TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


