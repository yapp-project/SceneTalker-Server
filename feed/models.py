from django.db import models
from drama.models import Drama


class Feed(models.Model):
    drama = models.OneToOneField(Drama, on_delete=models.CASCADE)


class Post(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
