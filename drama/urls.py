from django.urls import path
from . import views

app_name = 'drama'
urlpatterns = [
    path('', views.DramaListCreateView.as_view()),
    path('<int:pk>/', views.DramaRetrieveUpdate.as_view()),
]
