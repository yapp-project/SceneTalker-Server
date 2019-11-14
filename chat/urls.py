from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('count/<int:drama_id>/<str:episode>/', view=views.GetDramaEachEpisodeCount.as_view()),
    path('<str:room_name>/<str:episode>/<str:user_name>/', views.room, name='room'),
]
