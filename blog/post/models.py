from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    title = models.TextField("Заголовок", max_length=140, unique=True)
    text = models.TextField("Текст", max_length=140, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author",
        verbose_name="Автор поста",
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title


class ReadPost(models.Model):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_id", verbose_name="Id поста"
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Id пользователя",
    )

    class Meta:
        verbose_name = "Прочитанный пост"
        verbose_name_plural = "Прочитанные посты"

    def __str__(self):
        return self.post_id


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "following"), name="Не получится это сделать"
            )
        ]
