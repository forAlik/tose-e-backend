from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="توضیحات API شما",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Swagger URLs:
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #API URLs:
    path('api/news/', include('apps.news.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/subnews/', include('apps.subnews.urls')),
    path('api/achievements/', include('apps.achievements.urls')),
    path('api/forms/', include('apps.forms.urls')),

    path("auth/api/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


    #Admin URLs:
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)