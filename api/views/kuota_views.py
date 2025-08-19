import csv
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from .models import KuotaGlobal, KuotaKapal, Kapal, JenisIkan

def check_permission(endpoint_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            perm = RolePermission(endpoint_name)
            if not perm.has_permission(request, None):
                return JsonResponse({"error": "Akses ditolak"}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# 1. Import kuota global per WPP
class ImportKuotaGlobalView(View):
    def post(self, request):
        try:
            csv_file = request.FILES.get("file")
            if not csv_file:
                return JsonResponse({"error": "File CSV tidak ditemukan"}, status=400)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            created, skipped = 0, 0
            with transaction.atomic():
                for row in reader:
                    wpp = row.get("wpp")
                    jenis_ikan = row.get("jenis_ikan")
                    kuota = row.get("kuota")

                    if not (wpp and jenis_ikan and kuota):
                        skipped += 1
                        continue

                    try:
                        ikan = JenisIkan.objects.get(nama=jenis_ikan)
                        KuotaGlobal.objects.update_or_create(
                            wpp=wpp,
                            jenis_ikan=ikan,
                            defaults={"kuota": kuota}
                        )
                        created += 1
                    except JenisIkan.DoesNotExist:
                        skipped += 1

            return JsonResponse({
                "message": "Import selesai",
                "created": created,
                "skipped": skipped
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# 2. Atur kuota per kapal
class AturKuotaKapalView(View):
    def post(self, request):
        try:
            no_buku_kapal = request.POST.get("no_buku_kapal")
            jenis_ikan = request.POST.get("jenis_ikan")
            kuota = request.POST.get("kuota")

            if not (no_buku_kapal and jenis_ikan and kuota):
                return JsonResponse({"error": "Data tidak lengkap"}, status=400)

            try:
                kapal = Kapal.objects.get(no_buku_kapal=no_buku_kapal)
                ikan = JenisIkan.objects.get(nama=jenis_ikan)
            except Kapal.DoesNotExist:
                return JsonResponse({"error": "Kapal tidak ditemukan"}, status=404)
            except JenisIkan.DoesNotExist:
                return JsonResponse({"error": "Jenis ikan tidak ditemukan"}, status=404)

            KuotaKapal.objects.update_or_create(
                kapal=kapal,
                jenis_ikan=ikan,
                defaults={"kuota": kuota}
            )

            return JsonResponse({"message": "Kuota kapal berhasil diatur"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
