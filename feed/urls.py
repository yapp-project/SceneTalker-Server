from django.urls import path
from . import views

app_name = 'feed'
urlpatterns = [
    path('<int:feed_id>/post/', views.PostListCreateAPIView.as_view()),
    path('<int:feed_id>/post/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:feed_id>/post/<int:post_id>/like/', views.PostLikesUpdateAPIView.as_view()),
    path('<int:feed_id>/post/<int:post_id>/comment/', views.CommentListCreateAPIView.as_view()),
    path('<int:feed_id>/post/<int:post_id>/comment/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
]
