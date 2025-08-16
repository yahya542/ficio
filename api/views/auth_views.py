from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from api.serializers.auth_serializer import RegisterSerializer, CustomTokenObtainPairSerializer
from api.models import CustomUser, Profile


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Ambil no_reg_bkp dari profile.kapal
        try:
            noregbkp = user.profile.kapal.no_reg_bkp
        except AttributeError:
            noregbkp = None  # jika user belum punya kapal/profile

        return Response({
            "message": "User berhasil daftar",
            "noregbkp": noregbkp
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    identifier = request.data.get('username/noreg_bkp')  # bisa username admin atau no_reg_bkp
    password = request.data.get('password')

    # Validasi input
    if not identifier or not password:
        return Response({"error": "identifier dan password wajib diisi"}, status=400)

    user_found = None
    matched_profile = None

    # 1️⃣ Cek admin dulu
    try:
        user = CustomUser.objects.get(username=identifier, role='admin')
        if user.check_password(password):
            user_found = user
        else:
            return Response({"error": "Password salah"}, status=401)
    except CustomUser.DoesNotExist:
        # 2️⃣ Cek user biasa
        profiles = Profile.objects.select_related('user', 'kapal').filter(kapal__no_reg_bkp=identifier)
        for profile in profiles:
            if profile.user.check_password(password):
                user_found = profile.user
                matched_profile = profile
                break
        if not user_found:
            return Response({"error": "Akun tidak ditemukan atau password salah"}, status=404)

    # Buat JWT token
    refresh = RefreshToken.for_user(user_found)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "id": user_found.id,
            "username": user_found.username,
            "email": user_found.email,
            "role": 'admin' if user_found.role == 'admin' else matched_profile.role if matched_profile else None,
            "kapal": matched_profile.kapal.no_reg_bkp if matched_profile and matched_profile.kapal else None
        }
    })