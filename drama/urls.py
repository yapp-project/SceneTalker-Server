from django.urls import path
from . import views

app_name = 'drama'
urlpatterns = [
    path('', views.DramaListCreateView.as_view()),
]
