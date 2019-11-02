from django.urls import path
from . import views

app_name = 'feed'
urlpatterns = [
    path('<int:feed>/post/', views.PostListCreateAPIView.as_view()),
    path('<int:feed>/post/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:feed>/post/<int:post>/comment/', views.CommentListCreateAPIView.as_view()),
    path('<int:feed>/post/<int:post>/comment/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
]
