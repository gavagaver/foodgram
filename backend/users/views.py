from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from foodgram.pagination import CustomPagination

from .models import Subscribe
from .serializers import CustomUserSerializer, SubscribeSerializer

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
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'DELETE':
            subscribe = get_object_or_404(
                Subscribe,
                user=user,
                author=author,
            )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = SubscribeSerializer(
            author,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        Subscribe.objects.create(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        url_path='subscriptions',
        methods=('GET',),
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(subscribe__user=user)
        pages = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={"request": request},
        )
        return self.get_paginated_response(serializer.data)
