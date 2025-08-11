from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth import authenticate
from django.conf import settings
from api.models import CustomUser  # pastikan sesuai lokasi model kamu


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('noreg_bkp', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        # set role default user
        user = CustomUser(**validated_data)
        user.role = 'user'  # set default role di sini
        user.set_password(password)
        user.save()
        return user



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    noreg_bkp = request.data.get('noreg_bkp')
    password = request.data.get('password')

    if not noreg_bkp or not password:
        return Response({'error': 'noreg_bkp dan password wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, noreg_bkp=noreg_bkp, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
