from django.urls import path, include
from .views import DramaListCreateView, DramaRetrieveUpdate

app_name = 'drama'
urlpatterns = [
    path('', DramaListCreateView.as_view(), name='DramaListCreateView'),
    path('<int:pk>/', DramaRetrieveUpdate.as_view(), name='DramaRetrieveUpdate'),
]
