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
    is_broadcasting = models.BooleanField(default=True)
    episode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-rating"]

    def __str__(self):
        return '제목: {}'.format(self.title)


class DramaEachEpisode(models.Model):
    drama = models.ForeignKey(Drama, on_delete=models.CASCADE, related_name='each_episodes')
    episode = models.CharField(max_length=20)
    soda_count = models.IntegerField(default=0)
    sweet_potato_count = models.IntegerField(default=0)

    def __str__(self):
        return '제목 : {}, 회차 : {}, 사이다 : {}개, 고구마 : {}개'.format(
            self.drama.title, self.episode, self.soda_count, self.sweet_potato_count)


class DramaEachEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DramaEachEpisode
        fields = (
            'episode',
            'soda_count',
            'sweet_potato_count'
        )


class DramaSerializer(TaggitSerializer, serializers.ModelSerializer):
    from feed.models import FeedSerializer
    feed = FeedSerializer(read_only=True)
    is_bookmarked_by_me = serializers.SerializerMethodField()
    broadcasting_day = TagListSerializerField()
    genre = TagListSerializerField()

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
            'is_broadcasting',
            'is_bookmarked_by_me',
            'episode',
            'created_at',
            'updated_at',
            'feed'
        )

    def get_is_bookmarked_by_me(self, drama):
        request_user = self.context['request'].user
        return drama in request_user.drama_bookmark.all()
