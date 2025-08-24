from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ..models import Kapal, TangkapanIkan, Profile, KuotaKapal
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
    if request.user.role in ['admin', 'auditori', 'regulator']:
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


@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def kapal_history(request, no_buku_kapal=None):
    if request.user.role in ['admin', 'auditori', 'regulator']:
        # Admin wajib input no_buku_kapal
        if not no_buku_kapal:
            return Response({"detail": "Admin harus menyertakan no_buku_kapal"}, status=400)
        try:
            kapal = Kapal.objects.get(no_buku_kapal=no_buku_kapal)
        except Kapal.DoesNotExist:
            return Response({"detail": "Kapal tidak ditemukan"}, status=404)
        tangkapan = TangkapanIkan.objects.filter(kapal=kapal).order_by('created_at')
    else:
        # User biasa, ambil tangkapan kapal miliknya
        tangkapan = TangkapanIkan.objects.filter(kapal__profiles__user=request.user).order_by('created_at')

    data = []
    for t in tangkapan:
        kuota = t.kuota  # KuotaKapal instance, bisa None
        data.append({
            "id": t.id,
            "tanggal": t.created_at,
            "jenis_ikan": t.jenis_ikan.nama,
            "weight": t.weight,
            "location": t.location.name,
            "jumlah": t.jumlah,
            "kuota_dialokasikan": kuota.kuota if kuota else None,
            "kuota_terpakai": kuota.kuota_terpakai if kuota else None,
            "sisa_kuota": kuota.sisa_kuota if kuota else None
        })

    return Response({
        "history": data
    })
