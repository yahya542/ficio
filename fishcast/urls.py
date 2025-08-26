# backend/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import FileResponse
import os
from api.views.auth_views import login, RegisterView  

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dokumentasi(request):
    file_path = os.path.join(BASE_DIR, "dokumentasi/dokumentasi_mentah.md")
    return FileResponse(open(file_path, 'rb'), as_attachment=False, filename="API_Fishcast.md")

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


    #dokumentasi 
    path("dokumentasi/", dokumentasi, name="dokumentasi"),

    # Swagger docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
