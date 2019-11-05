from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "user"
urlpatterns = [
    path("<str:username>/", view = views.UserViewSet.as_view()),
    path("bookmarkDrama/", view = views.GetRealTimeUserBestDrama.as_view()),
    path("<int:drama_id>/bookmark/", view=views.ToggleDramaBookmark.as_view()),
    path("<str:username>/upload/<str:filename>/", view = views.PutUserProfileImage.as_view()),
]