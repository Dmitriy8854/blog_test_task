from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Post, ReadPost, Subscription


class PostAdmin(ModelAdmin):
    list_display = ("title", "text", "author")
    list_filter = ("title", "text", "author")


class ReadPostAdmin(ModelAdmin):
    list_display = ("post_id", "user_id")
    list_filter = ("post_id", "user_id")


class SubscriptionAdmin(ModelAdmin):
    list_display = ("user", "following")
    list_filter = ("user", "following")


admin.site.register(Post, PostAdmin)
admin.site.register(ReadPost, ReadPostAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
