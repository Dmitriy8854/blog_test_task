from django.urls import include, path
from rest_framework import routers
from .views import PostViewSet, SubscriptionViewSet
from .yasg import urlpatterns as docs_url

router = routers.SimpleRouter()

router.register("posts", PostViewSet, basename="posts")
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += docs_url
