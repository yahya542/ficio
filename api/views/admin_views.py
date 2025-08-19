
import csv
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from ..models import Kapal, JenisIkan
import io
from django.db import IntegrityError

def is_admin_request(request):
    return request.user.is_authenticated and request.user.role == 'admin'




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_kapal_csv(request):
    # Cek admin
    if not is_admin_request(request):
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    # Cek file CSV
    if "file" not in request.FILES:
        return Response(
            {"detail": "File CSV harus diupload dengan key 'file'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES["file"]

    try:
        decoded_file = file.read().decode("utf-8-sig").splitlines()  # handle BOM
    except Exception:
        return Response(
            {"detail": "Gagal membaca file. Pastikan file CSV valid."},
            status=status.HTTP_400_BAD_REQUEST
        )

    reader = csv.DictReader(decoded_file)
    created, skipped = 0, 0
    skipped_items = []

    # Mapping header CSV ke field model
    field_map = {
        "no_buku_kapal": ["no buku", "no_buku_kapal", "nomor buku", "nomor kapal", "nomor_buku"],
        "nama_kapal": ["nama kapal", "nama_kapal", "nama"]
    }

    for row in reader:
        # Buat key CSV case-insensitive
        row_lower = {k.strip().lower(): v.strip() for k, v in row.items()}
        data = {}

        # Ambil value sesuai mapping
        for field, headers in field_map.items():
            for h in headers:
                if h.lower() in row_lower and row_lower[h.lower()]:
                    data[field] = row_lower[h.lower()]
                    break

        nomor = data.get("no_buku_kapal")
        nama = data.get("nama_kapal")

        if not nomor or not nama:
            skipped += 1
            skipped_items.append({"row": reader.line_num, "reason": "missing_field"})
            continue

        print("Row CSV:", row)
        print("Mapped data:", data)
        print("Nomor:", nomor, "Nama:", nama)

        # Gunakan get_or_create untuk mencegah IntegrityError
        try:
            obj, created_flag = Kapal.objects.get_or_create(
                no_buku_kapal=nomor,
                defaults={"nama_kapal": nama}
            )
            if created_flag:
                created += 1
            else:
                skipped += 1
                skipped_items.append(nomor)
        except Exception as e:
            skipped += 1
            skipped_items.append(nomor or f"error: {str(e)}")

    return Response({
        "status": "success",
        "created": created,
        "skipped": skipped,
        "skipped_items": skipped_items
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_jenis_ikan_csv(request):
    # Validasi hanya admin
    if not is_admin_request(request):
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    # Validasi file
    file = request.FILES.get("file")
    if not file:
        return Response({"detail": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Baca file CSV
    decoded_file = file.read().decode("utf-8")
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)

    created, skipped = 0, 0
    for row in reader:
        nama = row.get("nama")
        if not nama:
            continue  # skip baris kosong

        # Validasi unik
        if JenisIkan.objects.filter(nama__iexact=nama).exists():
            skipped += 1
            continue

        JenisIkan.objects.create(nama=nama)
        created += 1

    return Response({
        "message": "Import selesai",
        "created": created,
        "skipped": skipped
    }, status=status.HTTP_201_CREATED)