from rest_framework import serializers
from api.models import CustomUser, Profile, Kapal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import CustomUser, Profile
from rest_framework.views import APIView
from api.serializers.auth_serializer import RegisterSerializer



@permission_classes([AllowAny])
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'no_buku_kapal': getattr(user.profile.kapal, 'no_buku_kapal', None) if hasattr(user, 'profile') else None
                }
            }
            return Response(token_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    identifier = request.data.get('username/no_buku_kapal')  # username atau nomor kapal
    password = request.data.get('password')

    if not identifier or not password:
        return Response({"error": "identifier dan password wajib diisi"}, status=400)

    user_found = None
    matched_profile = None

    # 1️⃣ Cek admin pakai username
    try:
        user = CustomUser.objects.get(username=identifier, role='admin')
        if user.check_password(password):
            user_found = user
    except CustomUser.DoesNotExist:
        pass

    # 2️⃣ Cek user biasa pakai nomor_buku_kapal
    if not user_found:
        profiles = Profile.objects.select_related('user', 'kapal').filter(kapal__no_buku_kapal=identifier)
        if not profiles.exists():
            return Response({"error": "Akun tidak ditemukan atau password salah"}, status=404)

        # ambil profile pertama yang password cocok
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
            "kapal": matched_profile.kapal.no_buku_kapal if matched_profile and matched_profile.kapal else None
        }
    })
