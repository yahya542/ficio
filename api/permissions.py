from rest_framework.permissions import BasePermission

ROLE_ACCESS = {
    'admin': [
        'list_kapal', 'input_kapal', 'input_tangkapan',
        'list_jenis_ikan', 'list_wpp', 'kapal_history'
    ],
    'pemilik': ['list_kapal', 'register', 'login', 'kapal_history'],
    'nahkoda': ['list_kapal', 'register', 'login', 'kapal_history'],
    'auditor': ['list_kapal', 'kapal_history'],
    'regulator': ['list_kapal', 'kelola_kuota', 'kapal_history'],
    'super_user': ['manage_roles', 'update_permission'],
}


# Untuk endpoint generik / pakai view.basename
class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # tentukan role
        role = 'super_user' if request.user.is_superuser else getattr(request.user, "role", None)
        if role is None:
            return False

        allowed = ROLE_ACCESS.get(role, [])
        return '*' in allowed or getattr(view, "basename", None) in allowed


# Untuk endpoint spesifik (misalnya hanya boleh "input_kapal" atau "manage_roles")
def RolePermissionFactory(endpoint_name):
    class _RolePermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False

            role = 'super_user' if request.user.is_superuser else getattr(request.user, "role", None)
            if role is None:
                return False

            allowed = ROLE_ACCESS.get(role, [])
            return '*' in allowed or endpoint_name in allowed

    return _RolePermission
