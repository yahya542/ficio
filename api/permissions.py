from rest_framework.permissions import BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import CustomUser as User

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


# Ambil role user
def get_user_role(user):
    if user.is_superuser:
        return "super_user"
    try:
        return user.profile.role  # kalau Anda simpan role di Profile
    except Exception:
        return getattr(user, "role", None)  # fallback kalau ada field role di User


# Untuk endpoint spesifik
def RolePermissionFactory(endpoint_name):
    class _RolePermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False

            role = get_user_role(request.user)
            if role is None:
                return False

            allowed = ROLE_ACCESS.get(role, [])
            return "*" in allowed or endpoint_name in allowed
    return _RolePermission


@api_view(["GET", "PUT"])
@permission_classes([RolePermissionFactory("manage_roles")])
def manage_access(request):
    if request.method == "GET":
        # List semua user + role
        users = User.objects.all()
        data = []
        for user in users:
            role = getattr(user.profile, "role", None)
            data.append({
                "username": user.username,
                "role": role
            })
        return Response(data)

    elif request.method == "PUT":
        # Update role user
        username = request.data.get("username")
        new_role = request.data.get("role")

        if not username or not new_role:
            return Response({"error": "username dan role wajib diisi"}, status=400)

        if new_role not in ROLE_ACCESS:
            return Response({"error": f"Role {new_role} tidak valid"}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User tidak ditemukan"}, status=404)

        profile = user.profile
        profile.role = new_role
        profile.save()

        return Response({
            "message": f"Role user {username} berhasil diubah ke {new_role}",
            "permissions": ROLE_ACCESS[new_role]
        })

@api_view(["GET"])
def list_access (request):
   
    users = User.objects.all()
    data = []
    for user in users:
        role = get_user_role(user)
        permissions = ROLE_ACCESS.get(role, [])
        data.append({
            "username": user.username,
            "role": role,
            "permissions": permissions
        })
    return Response(data)