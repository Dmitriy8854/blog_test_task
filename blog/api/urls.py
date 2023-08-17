from django.urls import include, path
from rest_framework import routers
from .views import PostViewSet, SubscriptionViewSet, post_list, APIBlog
from rest_framework.authtoken import views

router = routers.SimpleRouter()

router.register("posts", PostViewSet, basename="posts")
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")

urlpatterns = [
    path("", include(router.urls)),
    path("list/<str:username>/", post_list),
    # path('list/', post_list),
    path("blog/", APIBlog.as_view()),
    path("api-token-auth/", views.obtain_auth_token),
]
