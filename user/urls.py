from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "user"
urlpatterns = [
    path("bookmarkDrama/", view = views.GetRealTimeUserBestDrama.as_view()),
    path("<str:username>/", view = views.UserViewSet.as_view()),
    path("<str:drama_title>/add/", view = views.AddDramaBookmark.as_view()),
    path("<str:drama_title>/remove/", view = views.RemoveDramaBookmark.as_view()),
    path("<str:username>/upload/<str:filename>/", view = views.PutUserProfileImage.as_view()),
]