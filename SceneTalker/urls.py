from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user/', include('user.urls')),
    path('chat/', include('chat.urls')),
    path('drama/', include('drama.urls'))
]
