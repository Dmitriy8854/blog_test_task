from django.shortcuts import render
from .serializers import (
    PostSerializer,
    SubscriptionSerializer,
    ReadPostSerializer,
)  # NewsFeedSerializer
from rest_framework import filters, viewsets
from post.models import Post, ReadPost, Subscription, User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        is_read = ReadPost.objects.filter(user_id=user, post_id=OuterRef("pk"))
        queryset = Post.objects.select_related("author").annotate(
            read=Exists(is_read),
        )
        return queryset

    # def get_queryset(self):
    #     user = self.request.user
    #     is_read = ReadPost.objects.filter(user_id=user, post_id=OuterRef("pk"))
    #     queryset = Post.objects.all().annotate(
    #         read=Exists(is_read),
    #     )
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # pagination_class = LimitOffsetPagination
    # permission_classes = (AuthorOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter
    # Пишем метод, а в декораторе разрешим работу со списком объектов
    # и переопределим URL на более презентабельный
    @action(detail=False, url_path="list-news")
    def list_news(self, request):
        post_list = Post.objects.select_related("author").filter(
            author__following__user=request.user
        )
        # Нужны только последние пять котиков белого цвета
        # sub = self.request.user.follower.select_related("following").all()
        # posts = Post.objects.filter(author=sub)
        # Передадим queryset cats сериализатору
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(post_list, many=True)
        return Response(serializer.data)

    #  @action(detail=True)
    # def list_news(self, request):
    #     user = self.request.user
    #     is_read = ReadPost.objects.filter(user_id=user, post_id=OuterRef("pk"))
    #     queryset = Post.objects.select_related("author").annotate(
    #         read=Exists(is_read),
    #     )
    #     return queryset

    @action(detail=False, url_path="list-news")
    def list_news(self, request):
        post_list = Post.objects.select_related("author").filter(
            author__following__user=request.user
        )
        # Нужны только последние пять котиков белого цвета
        # sub = self.request.user.follower.select_related("following").all()
        # posts = Post.objects.filter(author=sub)
        # Передадим queryset cats сериализатору
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(post_list, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])  # Разрешены только POST- и GET-запросы
def post_list(request, username):
    # us = request.user
    # r = us.username
    # post = get_object_or_404(User, username=username)
    # В случае POST-запроса добавим список записей в БД
    # if request.method == 'POST':
    #     post = Post.objects.get(id=id)
    # #     current_user = request.user
    # #     serializer = ReadPostSerializer(data=request.data)
    # #     if serializer.user_id == current_user.id and serializer.post_id == post.id:
    #     post.read = True
    #     post.save()
    #     return Response(serializer.data)
    post_list = Post.objects.select_related("author").filter(
        author__following__user=request.user
    )

    # serializer = get_serializer(post_list, many=True)
    serializer = PostSerializer(post_list, many=True)
    return Response(serializer.data)


class APIBlog(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


# def sale():
#     post_send.delay()


# ReadPostSerializer
# @action(detail=False, url_path="read")
# def read_post(self, request):
#     post = Post.objects.get(id=id)
#     current_user = request.user
#     serializer = ReadPostSerializer(data=request.data)
#     if serializer.user_id == current_user.id and serializer.post_id == post.id:
#         post.read = True
#         post.save()
#         return Response(serializer.data)
#     else:
#         post.read = False
#         post.save()
#         return Response(serializer.data)


#   def post(self, request, format=None):
#     msg_id = request.data.get('msg_id')
#     message = Message.objects.get(id=msg_id)
#     if message:
#         post.read = True
#         post.save()
#         message_response = MessageView().post(request)
#         return message_response
#     else:


# class ReadPostSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ReadPost
#         fields = ("post_id", "user_id")


# class Test(TestCase):
#     def test_redirect(self):
#         client = Client()
#         response = client.get("/checklist_GTD/archive/")
#         self.assertRedirects(response, "/expected_redirect/url", 302, 200)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    # def get_queryset(self):
    #     return self.request.user.follower.select_related("following").all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# class NewsFeedViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = NewsFeedSerializer
#     def get_queryset(self):
#         return self.request.user.follower.select_related('following').all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class SuViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = NewsFeedSerializer


#   serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

#     def get_queryset(self):
#         post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
#         return post.comments.select_related('author')

#     def perform_create(self, serializer):
#         post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
#         serializer.save(author=self.request.user, post=post)


# class FollowViewSet(viewsets.ModelViewSet):
#     serializer_class = FollowSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('following__username',)

#     def get_queryset(self):
#         return self.request.user.follower.select_related('following').all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# def get_queryset(self):
#     user = self.request.user
#     is_read = ReadPost.objects.filter(user_id=user, post_id=OuterRef("pk"))
#     queryset = (
#         Post.objects.select_related("author")
#         .prefetch_related("ingredients")
#         .annotate(
#             read=Exists(is_read),
#         )
#     )
#     return queryset
