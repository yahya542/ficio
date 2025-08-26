from rest_framework.permissions import BasePermission

ROLE_ACCESS = {
    'admin': ['lihat_kapal', 'input_kapal', 'input_tangkapan', 'list_jenis_ikan', 'list_wpp', 'kapal_history'],
    'pemilik': ['lihat_kapal', 'register', 'login', 'kapal_history'],
    'nahkoda': ['lihat_kapal', 'register', 'login', 'kapal_history'],
    'auditor': ['lihat_kapal', 'kapal_history'],
    'regulator': ['lihat_kapal', 'kelola_kuota', 'kapal_history'],
    'super_user': ['manage_roles', 'update_permission'],
}

# Untuk endpoint satu method / tanpa parameter
class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        allowed = ROLE_ACCESS.get(request.user.role, [])
        return '*' in allowed or view.basename in allowed  # atau cek nama view default

# Untuk endpoint yang butuh parameter khusus (factory)
def RolePermissionFactory(endpoint_name):
    class _RolePermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False
            allowed = ROLE_ACCESS.get(request.user.role, [])
            return '*' in allowed or (endpoint_name in allowed)
    return _RolePermission
