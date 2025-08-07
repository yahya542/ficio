from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Ship, Tangkapan
from .serializers import ShipSerializer, TangkapanSerializer
from .permissions import IsAdminViaAPIKeyOrAuthenticated

# USER input kapal
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def input_ship(request):
    serializer = ShipSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # otomatis ambil user dari token
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ADMIN melihat semua kapal
@api_view(['GET'])
@permission_classes([IsAdminViaAPIKeyOrAuthenticated])
def list_ships(request):
    ships = Ship.objects.all()
    serializer = ShipSerializer(ships, many=True)
    return Response(serializer.data)

# ADMIN input tangkapan
@api_view(['POST'])
@permission_classes([IsAdminViaAPIKeyOrAuthenticated])
def input_tangkapan(request):
    serializer = TangkapanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ADMIN lihat semua tangkapan
@api_view(['GET'])
@permission_classes([IsAdminViaAPIKeyOrAuthenticated])
def list_tangkapan(request):
    tangkapan = Tangkapan.objects.all()
    serializer = TangkapanSerializer(tangkapan, many=True)
    return Response(serializer.data)
