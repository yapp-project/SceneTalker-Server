from django.db import models
from django.conf import settings
from rest_framework import serializers
from drama.models import Drama


class Feed(models.Model):
    drama = models.OneToOneField(Drama, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.drama.title)


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'


class Post(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True)  # s3에 올라가게 해야함
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def like_count(self):
        return self.likes.all().count()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
