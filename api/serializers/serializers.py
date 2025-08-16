from rest_framework import serializers
from ..models import Kapal, JenisIkan, WPP, TangkapanIkan, CustomUser



class JenisIkanSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisIkan
        fields = ['id', 'nama_ikan']


class WPPSerializer(serializers.ModelSerializer):
    class Meta:
        model = WPP
        fields = ['kode', 'nama_wpp']


class KapalSerializer(serializers.ModelSerializer):
    pemilik = serializers.SerializerMethodField()

    class Meta:
        model = Kapal
        fields = ['id', 'nama_kapal', 'no_reg_bkp', 'no_buku_kapal', 'pemilik']

    def get_pemilik(self, obj):
        profile = obj.profiles.filter(role='pemilik_kapal').first()
        return profile.user.username if profile else None


class TangkapanIkanSerializer(serializers.Serializer):
    jenis_ikan_id = serializers.IntegerField()
    berat = serializers.FloatField()
    jumlah = serializers.IntegerField()
    wpp_id = serializers.IntegerField()

class InputTangkapanSerializer(serializers.Serializer):
    no_reg_bkp = serializers.CharField()
    tangkapan = TangkapanIkanSerializer(many=True)

    def validate_no_reg_bkp(self, value):
        if not Kapal.objects.filter(no_reg_bkp=value).exists():
            raise serializers.ValidationError("Kapal dengan noreg_bkp ini tidak ditemukan")
        return value

    def create(self, validated_data):
        kapal = Kapal.objects.get(no_reg_bkp=validated_data['no_reg_bkp'])
        created_items = []

        for item in validated_data['tangkapan']:
            ikan = JenisIkan.objects.get(id=item['jenis_ikan_id'])
            wpp = WPP.objects.get(code=item['wpp_id'])
            tangkapan_obj = TangkapanIkan.objects.create(
                kapal=kapal,
                jenis_ikan=ikan,
                weight=item['berat'],
                location=wpp
            )
            created_items.append({
                "jenis_ikan": ikan.nama,
                "berat": item['berat'],
                "jumlah": item['jumlah'],
                "wpp": wpp.name
            })

        return {
            "no_reg_bkp": kapal.no_reg_bkp,
            "tangkapan": created_items
        }