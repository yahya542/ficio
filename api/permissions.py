from rest_framework.permissions import BasePermission
from django.conf import settings

class IsAdminViaAPIKeyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        admin_key = request.headers.get("X-ADMIN-KEY")
        if admin_key and admin_key == settings.ADMIN_API_KEY:
            return True  # admin pakai API key langsung
        return request.user and request.user.is_authenticated
