from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import super_user
from rest_framework.response import Response
from django.contrib.auth.models import User
@api_view(["POST"])
@permission_classes([super_user]) 
def update_user_role(request):
    """
    Superuser bisa mengubah role user lain
    """
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

    # simpan role di profile
    profile = user.profile  
    profile.role = new_role
    profile.save()

    return Response({
        "message": f"Role user {username} berhasil diubah ke {new_role}",
        "permissions": ROLE_ACCESS[new_role]
    }, status=200)