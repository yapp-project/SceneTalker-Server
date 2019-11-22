# chat/routing.py
from django.conf.urls import url
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:drama_id>/<str:episode>/<int:user_id>/', consumers.ChatConsumer),
]