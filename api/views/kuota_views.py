from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import KuotaKapal, Kapal
from rest_framework.serializers import Serializer, CharField, FloatField, ValidationError
from ..serializers.kuota_serializer import KuotaKapalInputSerializer



# Permission khusus regulator
class IsRegulator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'regulator'

# APIView untuk mengatur kuota kapal
class AturKuotaKapalView(APIView):
    permission_classes = [IsRegulator]

    def post(self, request):
        serializer = KuotaKapalInputSerializer(data=request.data)
        if serializer.is_valid():
            kuota = serializer.save()
            return Response({
                "message": "Kuota total kapal berhasil diatur",
                "no_buku_kapal": kuota.kapal.no_buku_kapal,
                "kuota": kuota.kuota,
                "kuota_terpakai": kuota.kuota_terpakai,
                "sisa_kuota": kuota.sisa_kuota
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
