# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from api.views.auth_views import  login, RegisterView 
from api.views.views import input_kapal, list_kapal, input_tangkapan_batch, list_tangkapan
from api.serializers.auth_serializer import RegisterSerializer



urlpatterns = [
     path('register/', RegisterView.as_view(), name='register'), 
    path('login/', login, name='login'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # semua API dari file api/urls.py
]
