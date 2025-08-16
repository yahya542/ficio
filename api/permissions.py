from rest_framework.permissions import BasePermission

ROLE_ACCESS = {
    'admin': ['*'],  # semua endpoint
    'pemilik_kapal': ['lihat_kapal', 'lihat_tangkapan', 'register', 'login'],
    'nahkoda': ['lihat_kapal',  'lihat_tangkapan', 'register', 'login'],
}

class RolePermission(BasePermission):
    def __init__(self, endpoint_name):
        self.endpoint_name = endpoint_name

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        allowed = ROLE_ACCESS.get(request.user.role, [])
        return '*' in allowed or self.endpoint_name in allowed
