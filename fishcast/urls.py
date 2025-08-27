from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.http import FileResponse
import os
from api.views.auth_views import login, RegisterView  

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dokumentasi(request):
    file_path = os.path.join(BASE_DIR, "dokumentasi/dokumentasi_mentah.md")
    return FileResponse(open(file_path, 'rb'), as_attachment=False, filename="API_Fishcast.md")

def blockchain_features(request):
    file_path = os.path.join(BASE_DIR, "dokumentasi/blockchain_supply_chain_features.md")
    return FileResponse(open(file_path, 'rb'), as_attachment=False, filename="blockchain_supply_chain_features.md")

urlpatterns = [
    # Auth
    path("register/", RegisterView.as_view(), name="register"), 
    path("login/", login, name="login"),

    # Django Admin
    path("admin/", admin.site.urls),

    # Semua API dari aplikasi api/urls.py
    path("api/", include("api.urls")),

    # Dokumentasi custom (file markdown)
    path("dokumentasi/", dokumentasi, name="dokumentasi"),
    path("blockchain-features/", blockchain_features, name="blockchain_features"),

    # 🔹 Schema (JSON/YAML)
    path("schema/", SpectacularAPIView.as_view(), name="schema"),

    # 🔹 Swagger UI
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # 🔹 Redoc UI
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]