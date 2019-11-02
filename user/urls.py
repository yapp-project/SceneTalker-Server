from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("bookmarkDrama/", view = views.GetRealTimeUserBestDrama.as_view()),
    path("<str:username>/", view = views.UserViewSet.as_view()),
    path("<str:drama_title>/add/", view = views.AddDramaBookmark.as_view()),
    path("<str:drama_title>/remove/", view = views.RemoveDramaBookmark.as_view()),
]