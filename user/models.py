from django.db import models
from django.contrib.auth.models import AbstractUser
from drama.models import Drama

# Create your models here.
class User(AbstractUser) :

    profile_image = models.ImageField(null=True, blank=True, upload_to='user_profile_image/')
    drama_bookmark = models.ManyToManyField(Drama, blank=True)

    def __str__(self) :
        return '이메일 : {} , 닉네임 : {}'.format(self.email, self.username)
