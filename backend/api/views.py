from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient

from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter
from .permissions import IsAdminOrReadOnly
from .serializers import IngredientSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
