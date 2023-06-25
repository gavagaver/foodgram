from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from foodgram.pagination import CustomPagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import User, Subscribe
from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    @action(
        detail=True,
        url_path='subscribe',
        methods=('POST', 'DELETE'),
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'DELETE':
            Subscribe.objects.filter(user=request.user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        Subscribe.objects.create(user=request.user, author=author)
        serializer = CustomUserSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
