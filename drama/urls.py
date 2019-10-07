from django.urls import path, include
from .views import test

app_name = 'drama'
urlpatterns = [
    path('', test, name='test'),
]
