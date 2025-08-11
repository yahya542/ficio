from rest_framework import serializers
from .models import Kapal, JenisIkan, WPP, TangkapanIkan


class JenisIkanSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisIkan
        fields = ['id', 'nama_ikan']


class WPPSerializer(serializers.ModelSerializer):
    class Meta:
        model = WPP
        fields = ['kode', 'nama_wpp']


class KapalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kapal
        fields = ['id', 'nama_kapal', 'pemilik']


# Serializer untuk tiap tangkapan
class TangkapanIkanSerializer(serializers.Serializer):
    ikan_id = serializers.IntegerField()
    berat = serializers.IntegerField()
    lokasi_id = serializers.IntegerField()

    def validate(self, data):
        # Validasi ikan
        if not JenisIkan.objects.filter(id=data['ikan_id']).exists():
            raise serializers.ValidationError({"ikan_id": "Jenis ikan tidak ditemukan"})
        # Validasi lokasi/WPP
        if not WPP.objects.filter(kode=data['lokasi_id']).exists():
            raise serializers.ValidationError({"lokasi_id": "Lokasi WPP tidak ditemukan"})
        return data


# Serializer utama untuk input batch
class InputTangkapanSerializer(serializers.Serializer):
    id_kapal = serializers.IntegerField()
    tangkapan = TangkapanIkanSerializer(many=True)

    def validate_id_kapal(self, value):
        if not Kapal.objects.filter(id=value).exists():
            raise serializers.ValidationError("Kapal tidak ditemukan")
        return value

    def create(self, validated_data):
        kapal = Kapal.objects.get(id=validated_data['id_kapal'])
        tangkapan_list = validated_data['tangkapan']

        created_items = []
        for item in tangkapan_list:
            ikan = JenisIkan.objects.get(id=item['ikan_id'])
            wpp = WPP.objects.get(kode=item['lokasi_id'])
            tangkapan_obj = TangkapanIkan.objects.create(
                kapal=kapal,
                jenis_ikan=ikan,
                jumlah=item['berat'],
                wpp=wpp
            )
            created_items.append(tangkapan_obj)
        return created_items
