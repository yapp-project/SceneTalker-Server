from django.contrib import admin
from .models import Feed, Post, Comment

admin.site.register(Feed)
admin.site.register(Post)
admin.site.register(Comment)