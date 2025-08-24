from rest_framework import serializers
from api.models import CustomUser, Profile, Kapal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import CustomUser, Profile
from rest_framework.views import APIView
from api.serializers.auth_serializer import RegisterSerializer, CustomTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'no_buku_kapal': getattr(user.profile.kapal, 'no_buku_kapal', None) 
                                     if hasattr(user, 'profile') else None
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer_class = CustomTokenObtainPairSerializer
    
    identifier = request.data.get('username/no_buku_kapal')  # username atau nomor kapal
    password = request.data.get('password')

    if not identifier or not password:
        return Response({"error": "identifier dan password wajib diisi"}, status=400)

    user_found = None
    kapal_no = None

    # 1️⃣ Cek username (admin, auditori, regulator)
    try:
        user = CustomUser.objects.get(username=identifier)
        if user.check_password(password):
            user_found = user
            if user.role not in ['pemilik_kapal', 'nahkoda']:
                kapal_no = None
    except CustomUser.DoesNotExist:
        pass

    # 2️⃣ Cek no_buku_kapal (pemilik_kapal / nahkoda)
    if not user_found:
        profiles = Profile.objects.select_related('user', 'kapal').filter(kapal__no_buku_kapal=identifier)
        for profile in profiles:
            if profile.user.check_password(password):
                user_found = profile.user
                kapal_no = profile.kapal.no_buku_kapal
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
            "role": user_found.role,
            "kapal": kapal_no
        }
    })

