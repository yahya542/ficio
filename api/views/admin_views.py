
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

    for idx, row in enumerate(reader, start=2):  # start=2 karena baris header
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
            skipped_items.append({"row": idx, "reason": "missing_field"})
            print(f"Baris {idx}: dilewati (missing field) → {row}")
            continue

        # Gunakan get_or_create untuk mencegah duplikat
        try:
            obj, created_flag = Kapal.objects.get_or_create(
                no_buku_kapal=nomor,
                defaults={"nama_kapal": nama}
            )
            if created_flag:
                created += 1
                print(f"Baris {idx}: berhasil dibuat → Nomor: {nomor}, Nama: {nama}")
            else:
                skipped += 1
                skipped_items.append({"row": idx, "reason": "duplicate", "no_buku_kapal": nomor})
                print(f"Baris {idx}: dilewati (duplikat) → Nomor: {nomor}, Nama: {nama}")
        except Exception as e:
            skipped += 1
            skipped_items.append({"row": idx, "reason": f"error: {str(e)}", "no_buku_kapal": nomor})
            print(f"Baris {idx}: dilewati (error) → Nomor: {nomor}, Nama: {nama}, Error: {str(e)}")

    print(f"Import selesai: {created} dibuat, {skipped} dilewati")
    return Response({
        "status": "success",
        "created": created,
        "skipped": skipped,
        "skipped_items": skipped_items
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_jenis_ikan_csv(request):
    if not is_admin_request(request):
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    file = request.FILES.get("file")
    if not file:
        return Response({"detail": "CSV file is required"}, status=status.HTTP_400_BAD_REQUEST)

    decoded_file = file.read().decode("utf-8-sig")  # handle BOM
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)

    created, skipped = 0, 0
    for idx, row in enumerate(reader, start=2):  # start=2 karena baris header
        nama = row.get("nama")
        if not nama:
            skipped += 1
            print(f"Baris {idx}: dilewati (missing 'nama')")
            continue

        if JenisIkan.objects.filter(nama__iexact=nama).exists():
            skipped += 1
            print(f"Baris {idx}: dilewati (duplikat) → {nama}")
            continue

        JenisIkan.objects.create(nama=nama)
        created += 1
        print(f"Baris {idx}: berhasil dibuat → {nama}")

    print(f"Import selesai: {created} dibuat, {skipped} dilewati")
    return Response({
        "message": "Import selesai",
        "created": created,
        "skipped": skipped
    }, status=status.HTTP_201_CREATED)
