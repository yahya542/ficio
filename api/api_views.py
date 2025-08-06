from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import user_passes_test
from .models import Ship, Ikan
from .serializers import ShipSerializer, IkanSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_input_ship(request):
    data = request.data
    data['user'] = request.user.id  # Auto assign ke user yang login
    serializer = ShipSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def admin_only(user):
    return user.is_staff

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(admin_only)
def admin_input_tangkapan(request):
    data = request.data
    try:
        ship = Ship.objects.get(id=data.get('ship_id'))
    except Ship.DoesNotExist:
        return Response({"error": "Ship not found."}, status=status.HTTP_404_NOT_FOUND)

    ikan = Ikan.objects.create(
        jenis_ikan=data.get('jenis_ikan'),
        jumlah=data.get('jumlah'),
        lokasi_tangkap=data.get('lokasi_tangkap'),
        ship=ship
    )
    serializer = IkanSerializer(ikan)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
