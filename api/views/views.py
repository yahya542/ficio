from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..models import Kapal, TangkapanIkan, Profile, KuotaKapal
from ..serializers.serializers import KapalSerializer, InputTangkapanSerializer, JenisIkanSerializer, WPPSerializer
from ..permissions import RolePermission, RolePermissionFactory
from django.db.models import Sum

def is_admin_request(request):
    return request.user.is_authenticated and request.user.role == 'admin'



@api_view(['POST'])
@permission_classes([RolePermissionFactory('input_kapal')])
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
@permission_classes([RolePermission('list_kapal')])
def list_kapal(request):
    if request.user.role in ['admin', 'auditori', 'regulator']:
        kapal = Kapal.objects.all()
    else:
        kapal = Kapal.objects.filter(profiles__user=request.user)
    serializer = KapalSerializer(kapal, many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([RolePermission('input_tangkapan')])
def input_tangkapan_batch(request):
    if not is_admin_request(request):
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    serializer = InputTangkapanSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.save()  # result dict {"no_buku_kapal": ..., "tangkapan": [...]}

        kuota = KuotaKapal.objects.filter(
            kapal__no_buku_kapal=result['no_buku_kapal']
        ).first()

        # Hitung total berat batch (sebagai kuota terpakai batch ini)
        total_berat_batch = sum([t['berat'] for t in result['tangkapan']])

        for t in result['tangkapan']:
            if kuota:
                t['kuota_dialokasikan'] = kuota.kuota
                t['kuota_terpakai'] = t['berat']  # kuota terpakai per item = berat item
                # sisa kuota per item tidak relevan, bisa None atau sama seperti summary
                t['sisa_kuota'] = kuota.kuota - total_berat_batch
            else:
                t['kuota_dialokasikan'] = None
                t['kuota_terpakai'] = t['berat']
                t['sisa_kuota'] = None

        # Summary pakai total batch
        result['summary'] = {
            "kuota_dialokasikan": kuota.kuota if kuota else None,
            "kuota_terpakai": total_berat_batch,
            "sisa_kuota_terhitung": (kuota.kuota - total_berat_batch) if kuota else None,
        }

        return Response({
            "message": "Tangkapan berhasil disimpan",
            "data": result
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
@permission_classes([RolePermission('list_jenis_ikan')])
def list_jenis_ikan(request):
    ikan = JenisIkanSerializer.Meta.model.objects.all()
    serializer = JenisIkanSerializer(ikan, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([RolePermission('list_wpp')])
def list_wpp(request):
    wpp = WPPSerializer.Meta.model.objects.all()
    serializer = WPPSerializer(wpp, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([RolePermissionFactory('kapal_history')])
def kapal_history(request, no_buku_kapal=None):
    # Tentukan kapal berdasarkan role
    if request.user.role in ['admin', 'auditor', 'regulator']:
        if not no_buku_kapal:
            return Response({"detail": "Admin harus menyertakan no_buku_kapal"}, status=400)
        kapal = Kapal.objects.filter(no_buku_kapal=no_buku_kapal).first()
        if not kapal:
            return Response({"detail": "Kapal tidak ditemukan"}, status=404)
        tangkapan = TangkapanIkan.objects.filter(kapal=kapal).order_by('created_at')
    else:  # pemilik_kapal / nahkoda
        kapal = Kapal.objects.filter(profiles__user=request.user).first()
        if not kapal:
            return Response({"detail": "Kapal milik user tidak ditemukan"}, status=404)
        tangkapan = TangkapanIkan.objects.filter(kapal=kapal).order_by('created_at')

    data = []
    for t in tangkapan:
        kuota_dialokasikan = t.kuota.kuota if hasattr(t, 'kuota') and t.kuota else None
        kuota_terpakai = t.kuota.kuota_terpakai if hasattr(t, 'kuota') and t.kuota else None
        sisa_kuota = kuota_dialokasikan - t.weight if kuota_dialokasikan else None

        # Logging ke console
        print(f"Tangkapan ID {t.id}: tanggal={t.created_at}, jenis={t.jenis_ikan.nama}, weight={t.weight}, kapal={kapal.no_buku_kapal}")

        data.append({
            "id": t.id,
            "tanggal": t.created_at,
            "jenis_ikan": t.jenis_ikan.nama,
            "weight": t.weight,
            "location": t.location.name,
            "kuota_dialokasikan": kuota_dialokasikan,
            "kuota_terpakai": kuota_terpakai,
            "sisa_kuota": sisa_kuota
        })

    return Response({"history": data})