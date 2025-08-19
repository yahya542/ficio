# serializers.py
from rest_framework import serializers
from .models import KuotaGlobal, KuotaKapal

class KuotaGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = KuotaGlobal
        fields = ['id', 'wpp', 'jenis_ikan', 'jumlah_kuota']


class KuotaKapalSerializer(serializers.ModelSerializer):
    no_buku_kapal = serializers.CharField(source='kapal.no_buku_kapal', read_only=True)

    class Meta:
        model = KuotaKapal
        fields = ['id', 'kapal', 'no_buku_kapal', 'jenis_ikan', 'kuota_dialokasikan', 'kuota_terpakai']
        read_only_fields = ['kuota_terpakai']
