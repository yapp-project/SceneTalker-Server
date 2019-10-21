from django.db import models
from django.conf import settings
from drama.models import Drama


class Feed(models.Model):
    drama = models.OneToOneField(Drama, on_delete=models.CASCADE)


class Post(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField()  # s3에 올라가게 해야함
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_likes_count(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
