from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
