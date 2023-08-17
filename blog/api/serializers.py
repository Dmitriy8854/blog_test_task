from post.models import Post, ReadPost, Subscription, User
from rest_framework import serializers
from rest_framework.serializers import (
    BooleanField,
    ModelSerializer,
    SerializerMethodField,
)
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


class ReadPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadPost
        fields = ("post_id", "user_id")


class PostSerializer(serializers.ModelSerializer):
    # read = ReadPostSerializer(read_only=True, many=True)
    is_read = serializers.SerializerMethodField()
    # author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    # author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("title", "text", "author", "creation_date", "is_read")

    def get_is_read(request):
        # def is_read(request, kwargs):
        user = request.user
        post = get.kwargs
        return ReadPost.objects.get(post_id=post.id, user_id=user.id).exists()
        # you need to provide the user and the article objects


class SubscriptionSerializer(serializers.ModelSerializer):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    following = SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        fields = "__all__"
        model = Subscription
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Subscription.objects.all(), fields=("user", "following")
        #     )
        # ]

    # def validate(self, data):
    #     if data["user"] == data["following"]:
    #         raise serializers.ValidationError("Имя не может совпадать с именем автора!")
    #     return data


# c = Client
# class Read(serializers.Field):
#     # При чтении данных ничего не меняем - просто возвращаем как есть

#     def to_representation(self, value):
#         return value

#     # При записи код цвета конвертируется в его название
#     def to_internal_value(self, data):
#         # Доверяй, но проверяй
#         try:
#             # Если имя цвета существует, то конвертируем код в название
#             data = webcolors.hex_to_name(data)
#         except ValueError:
#             # Иначе возвращаем ошибку
#             raise serializers.ValidationError("Для этого цвета нет имени")
#         # Возвращаем данные в новом формате
#         return data

#     def read(self):
#         client = request.user()
#         client.id
#         response = client.get("/posts/{post.id}/")
#         if readpost.post_id == client:

#         self.assertRedirects(response, "/expected_redirect/url", 302, 200)
