from django.urls import path
from . import views

app_name = 'drama'
urlpatterns = [
    path('', views.DramaListView.as_view()),
    path('<int:drama_id>/each-episode/', views.DramaEachEpisodeList.as_view())
]
