from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="ScenteTalker API",
        default_version='v1',
        description="ScenteTalker Open API 문서 페이지 입니다.",
        contact=openapi.Contact(email="bjq913@gmail.com"),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user/', include('user.urls')),
    path('chat/', include('chat.urls')),
    path('drama/', include('drama.urls')),
    path('feed/', include('feed.urls')),

    # Auto DRF API docs
    url(r'^swagger(?P<format>\.json|\.yaml)/v1$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/v1/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/v1/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
