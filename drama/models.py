from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from rest_framework import serializers


class TaggedGenre(TaggedItemBase):
    content_object = models.ForeignKey('Drama', on_delete=models.CASCADE)


class TaggedBroadCastingDay(TaggedItemBase):
    content_object = models.ForeignKey('Drama', on_delete=models.CASCADE)


class Drama(models.Model):
    title = models.CharField(max_length=50)
    summary = models.TextField()
    genre = TaggableManager(through=TaggedGenre, related_name='genre')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    poster_url = models.URLField(max_length=250)
    broadcasting_day = TaggableManager(through=TaggedBroadCastingDay, related_name='broadcasting_day')
    broadcasting_start_time = models.TimeField()
    broadcasting_end_time = models.TimeField()
    broadcasting_station = models.CharField(max_length=20)
    is_broadcasiting = models.BooleanField(default=True)
    episode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-rating"]

    def __str__(self):
        return '제목: {}'.format(self.title)


class DramaSerializer(TaggitSerializer, serializers.ModelSerializer):
    from feed.models import FeedSerializer
    broadcasting_day = TagListSerializerField()
    genre = TagListSerializerField()
    feed = FeedSerializer(read_only=True)

    class Meta:
        model = Drama
        fields = (
            'id',
            'title',
            'summary',
            'genre',
            'rating',
            'poster_url',
            'broadcasting_day',
            'broadcasting_start_time',
            'broadcasting_end_time',
            'broadcasting_station',
            'is_broadcasiting',
            'episode',
            'created_at',
            'updated_at',
            'feed'
        )
