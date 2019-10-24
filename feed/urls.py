from django.urls import path
from . import views

app_name = 'feed'
urlpatterns = [
    path('<int:feed_id>/post/', views.PostListCreateAPIView.as_view()),
    path('<int:feed_id>/post/<int:post_id>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:feed_id>/post/<int:post_id>/comment/', views.CommentListCreateAPIView.as_view()),
    path('<int:feed_id>/post/<int:post_id>/comment/<int:comment_id>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
]
