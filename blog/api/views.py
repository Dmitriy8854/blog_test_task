from django.shortcuts import render
from .serializers import (
    PostSerializer,
    SubscriptionSerializer,
    ReadPostSerializer,
)

from rest_framework import filters, viewsets
from post.models import Post, ReadPost, Subscription, User
from django.test import TestCase, Client
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef
from rest_framework.response import Response


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def read(self, request, **kwargs):
        user = request.user
        post = get_object_or_404(Post, id=self.kwargs.get("pk"))
        serializer = ReadPostSerializer(post, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        ReadPost.objects.create(post_id=post, user_id=user)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(detail=False, url_path="list-news")
    def list_news(self, request):
        post_list = Post.objects.select_related("author").filter(
            author__following__user=request.user
        )
        serializer = self.get_serializer(post_list, many=True)
        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    # def get_queryset(self):
    #     return self.request.user.follower.select_related("following").all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
