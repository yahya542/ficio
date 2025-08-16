from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..models import Kapal, TangkapanIkan, Profile
from ..serializers.serializers import KapalSerializer, InputTangkapanSerializer, JenisIkanSerializer, WPPSerializer
from ..permissions import RolePermission

def is_admin_request(request):
    return request.user.is_authenticated and request.user.role == 'admin'



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def input_kapal(request):
    serializer = KapalSerializer(data=request.data)
    if serializer.is_valid():
        kapal = serializer.save()
        # Buat profile pemilik kapal jika belum ada
        Profile.objects.get_or_create(
            user=request.user,
            kapal=kapal,
            role='pemilik_kapal'
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_kapal(request):
    if is_admin_request(request):
        kapal = Kapal.objects.all()
    else:
        kapal = Kapal.objects.filter(profiles__user=request.user)
    serializer = KapalSerializer(kapal, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def input_tangkapan_batch(request):
    if not is_admin_request(request):
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    serializer = InputTangkapanSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.save()  # result sudah dict {"no_reg_bkp": ..., "tangkapan": [...]}
        return Response({
            "message": "Tangkapan berhasil disimpan",
            "data": result
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tangkapan(request):
    if is_admin_request(request):
        tangkapan = TangkapanIkan.objects.all()
    else:
        tangkapan = TangkapanIkan.objects.filter(kapal__profiles__user=request.user)
    data = [{
        "kapal": t.kapal.nama_kapal,
        "jenis_ikan": t.jenis_ikan.nama,
        "weight": t.weight,
        "location": t.location.name,
    } for t in tangkapan]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_jenis_ikan(request):
    ikan = JenisIkanSerializer.Meta.model.objects.all()
    serializer = JenisIkanSerializer(ikan, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_wpp(request):
    wpp = WPPSerializer.Meta.model.objects.all()
    serializer = WPPSerializer(wpp, many=True)
    return Response(serializer.data)


#console 
