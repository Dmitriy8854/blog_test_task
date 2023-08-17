from post.models import Post, ReadPost, Subscription, User
from rest_framework import serializers
from rest_framework.serializers import (
    BooleanField,
    ModelSerializer,
    SerializerMethodField,
)
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class ReadPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "text", "author")
        read_only_fields = ("title", "text", "author")


class PostSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("title", "text", "author", "creation_date", "is_read")

    def get_is_read(self, obj):
        request = self.context.get("request")
        user = request.user
        return ReadPost.objects.filter(post_id=obj.id, user_id=user.id).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    following = SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        fields = "__all__"
        model = Subscription
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(), fields=("user", "following")
            )
        ]

    def validate(self, data):
        if data["user"] == data["following"]:
            raise serializers.ValidationError("Имя не может совпадать с именем автора!")
        return data
