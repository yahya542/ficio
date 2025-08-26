from rest_framework import serializers
from ..models import Kapal, JenisIkan, WPP, TangkapanIkan, CustomUser, KuotaKapal



class JenisIkanSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisIkan
        fields = ['id', 'nama']


class WPPSerializer(serializers.ModelSerializer):
    class Meta:
        model = WPP
        fields = ['code', 'name']


class KapalSerializer(serializers.ModelSerializer):
    pemilik = serializers.SerializerMethodField()

    class Meta:
        model = Kapal
        fields = ['id', 'nama_kapal', 'no_buku_kapal', 'no_buku_kapal', 'pemilik']

    def get_pemilik(self, obj):
        profile = obj.profiles.filter(role='pemilik_kapal').first()
        return profile.user.username if profile else None


class TangkapanIkanSerializer(serializers.Serializer):
    jenis_ikan_id = serializers.IntegerField()
    berat = serializers.FloatField()
    wpp_id = serializers.IntegerField()


class InputTangkapanSerializer(serializers.Serializer):
    no_buku_kapal = serializers.CharField()
    tangkapan = serializers.ListField()

    def validate_no_buku_kapal(self, value):
        if not Kapal.objects.filter(no_buku_kapal=value).exists():
            raise serializers.ValidationError("Kapal dengan noreg_bkp ini tidak ditemukan")
        return value

    def create(self, validated_data):
        kapal = Kapal.objects.get(no_buku_kapal=validated_data['no_buku_kapal'])
        created_items = []

        # Ambil kuota kapal
        kuota = KuotaKapal.objects.filter(kapal=kapal).first()
        if not kuota:
            raise serializers.ValidationError("Kuota kapal belum diatur")
        kuota_dialokasikan = kuota.kuota
        kuota_terpakai = kuota.kuota_terpakai
        sisa_kuota = kuota_dialokasikan - kuota_terpakai

        # Hitung total berat batch baru
        total_berat_batch = sum(item['berat'] for item in validated_data['tangkapan'])
        if total_berat_batch > sisa_kuota:
            raise serializers.ValidationError(
                f"Kuota kapal tidak mencukupi. Sisa: {sisa_kuota} kg, total batch: {total_berat_batch} kg"
            )

        # Simpan tangkapan batch
        for item in validated_data['tangkapan']:
            ikan = JenisIkan.objects.get(id=item['jenis_ikan_id'])
            wpp = WPP.objects.get(code=item['wpp_id'])
            tangkapan_obj = TangkapanIkan.objects.create(
                kapal=kapal,
                jenis_ikan=ikan,
                weight=item['berat'],
                location=wpp,
                kuota=kuota
            )
            created_items.append({
                "jenis_ikan": ikan.nama,
                "berat": item['berat'],
                "wpp": wpp.name,
                "kuota_dialokasikan": kuota_dialokasikan,
                "kuota_terpakai": kuota_terpakai,
                "sisa_kuota": sisa_kuota - total_berat_batch
            })

        # Update kuota_terpakai di KuotaKapal
        kuota.kuota_terpakai += total_berat_batch
        kuota.save()

        return {
            "no_buku_kapal": kapal.no_buku_kapal,
            "tangkapan": created_items,
            "summary": {
                "total_berat_batch": total_berat_batch,
                "kuota_dialokasikan": kuota_dialokasikan,
                "kuota_terpakai": kuota_terpakai + total_berat_batch,
                "sisa_kuota_terhitung": sisa_kuota - total_berat_batch
            }
        }




class TangkapanHistorySerializer(serializers.ModelSerializer):
    jenis_ikan = serializers.CharField(source='jenis_ikan.nama')
    wpp = serializers.CharField(source='location.name')

    class Meta:
        model = TangkapanIkan
        fields = ['jenis_ikan', 'weight',  'wpp', 'created_at']
