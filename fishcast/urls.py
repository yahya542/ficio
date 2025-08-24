# backend/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# import views kamu
from api.views.auth_views import login, RegisterView  

schema_view = get_schema_view(
   openapi.Info(
      title="Sistem Kapal API",
      default_version='v1',
      description="Dokumentasi API untuk kapal, tangkapan, auth, dan kuota",
      contact=openapi.Contact(email="support@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', login, name='login'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Semua API dari aplikasi api/urls.py
    path('api/', include('api.urls')),

    # Swagger docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
