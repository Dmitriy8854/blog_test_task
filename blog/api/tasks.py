from blog.celery import app
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from post.models import Post, User


@app.task
def post_send():
    user = User.objects.all()
    post_list = Post.objects.select_related("author").filter(
        author__following__user=user
    )[:5]
    if len(post_list) > 0:
        send_mail(
            subject=f"Ежедневная рассылка постов",
            message=(post_list.text),
            from_email="dmitrt300@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
    else:
        raise ValueError("Список пуст")
