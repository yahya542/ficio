from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Ship, Tangkapan, Ikan
from .serializers import ShipSerializer, TangkapanSerializer, IkanSerializer, ShipDetailSerializer
from .permissions import IsAdminViaAPIKeyOrAuthenticated
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




#api tanpa auth 
class ReadOnlyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


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

#list nama ikan 
class IkanViewSet(viewsets.ModelViewSet):
    queryset = Ikan.objects.all()
    serializer_class = IkanSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

#admin key 
class IsAdminViaAPIKeyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        admin_key = (
            request.headers.get('X-ADMIN-KEY') or
            request.GET.get('X-ADMIN-KEY')  
        )
        if admin_key and admin_key == settings.ADMIN_API_KEY:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff



#cek validasi id kapal 
@api_view(['POST'])
@permission_classes([IsAdminViaAPIKeyOrAuthenticated])
def valid_id_view(request):
    # ✅ Ambil id_kapal dari body POST
    ship_id = request.data.get('ship_id')
    
    if not id:
        return Response({'error': 'id_kapal is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # ✅ GET data kapal sesuai id_kapal yang dikirim via POST
        ship_id = Ship.objects.get(ship_id=ship_id)
        serializer = ShipDetailSerializer(ship)
        return Response({
            'valid': True,
            'data': serializer.data
        })
    except Ship.DoesNotExist:
        return Response({
            'valid': False,
            'data': None
        })