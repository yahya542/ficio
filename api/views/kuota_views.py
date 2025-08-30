from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..serializers.kuota_serializer import KuotaKapalInputSerializer
from ..permissions import RolePermissionFactory
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Atur kuota kapal",
    request=KuotaKapalInputSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([RolePermissionFactory('kelola_kuota')])
def atur_kuota_kapal(request):
    serializer = KuotaKapalInputSerializer(data=request.data)
    if serializer.is_valid():
        kuota = serializer.save()
        return Response({
            "message": "Kuota  kapal berhasil diatur",
            "no_buku_kapal": kuota.kapal.no_buku_kapal,
            "kuota": kuota.kuota,
            "kuota_terpakai": kuota.kuota_terpakai,
            "sisa_kuota": kuota.sisa_kuota
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
