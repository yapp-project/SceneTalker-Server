from django.db import models
from taggit.managers import TaggableManager


class Drama(models.Model):
    title = models.CharField(max_length=50)
    summary = models.TextField()
    genre = TaggableManager()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    broadcasting_start_date = models.DateField()
    broadcasting_day = models.CharField(max_length=10)
    broadcasting_start_time = models.TimeField()
    broadcasting_end_time = models.TimeField()
    broadcasting_station = models.CharField(max_length=50)
    is_broadcasiting = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["rating"]

    def __str__(self):
        return '이름: {}, 평점: {}, 방영일: {}, 방영시간: {} ~ {}'.format(self.title, self.rating, self.broadcasting_day,
                                                               self.broadcasting_start_time, self.broadcasting_end_time)
