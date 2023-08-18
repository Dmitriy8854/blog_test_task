from blog.celery import app
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from post.models import Post, User
from django.shortcuts import get_object_or_404
from django.conf import settings


@app.task
def post_send():
    """Функция для отправки писем"""
    for user in User.objects.all():
        #     user = [i.id for i in User.objects.all()]
        # post_list = Post.objects.all()[:5]
        # post_list = Post.objects.select_related("author").filter(
        post_list = Post.objects.filter(author__following__user=user)[:5]
        post_str = "\n".join(
            [post.text for post in post_list],
        )

        send_mail(
            subject=f"Ежедневная рассылка постов",
            message=post_str,
            from_email="youremail@mail.ru",
            recipient_list=[user.email],
            fail_silently=False,
        )
