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
    username = serializers.CharField(source='pemilik.noreg_bkp', read_only=True)

    class Meta:
        model = Kapal
        fields = ['id', 'nama_kapal', 'pemilik', 'username', 'nahkoda', ]



# Serializer untuk tiap tangkapan
# Serializer untuk tiap tangkapan

class TangkapanIkanSerializer(serializers.Serializer):
    ikan_id = serializers.IntegerField()
    berat = serializers.FloatField()
    lokasi_id = serializers.IntegerField()

    def validate(self, data):
        if not JenisIkan.objects.filter(id=data['ikan_id']).exists():
            raise serializers.ValidationError({"ikan_id": "Jenis ikan tidak ditemukan"})
        if not WPP.objects.filter(code=data['lokasi_id']).exists():
            raise serializers.ValidationError({"lokasi_id": "Lokasi WPP tidak ditemukan"})
        return data


class InputTangkapanSerializer(serializers.Serializer):
    noreg_bkp = serializers.CharField()
    tangkapan = TangkapanIkanSerializer(many=True)

    def validate_noreg_bkp(self, value):
        try:
            # Gunakan get_by_natural_key supaya ikut setting USERNAME_FIELD
            user = CustomUser.objects.get_by_natural_key(value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User dengan noreg_bkp ini tidak ditemukan")
        
        if not Kapal.objects.filter(pemilik=user).exists():
            raise serializers.ValidationError("Tidak ada kapal yang dimiliki user ini")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.get_by_natural_key(validated_data['noreg_bkp'])
        kapal = Kapal.objects.filter(pemilik=user).first()
        if not kapal:
            raise serializers.ValidationError("Kapal tidak ditemukan untuk user ini")
        
        tangkapan_list = validated_data['tangkapan']
        created_items = []

        for item in tangkapan_list:
            ikan = JenisIkan.objects.get(id=item['ikan_id'])
            wpp = WPP.objects.get(code=item['lokasi_id'])
            tangkapan_obj = TangkapanIkan.objects.create(
                kapal=kapal,
                jenis_ikan=ikan,
                weight=item['berat'],
                location=wpp
            )
            created_items.append(tangkapan_obj)
        
        return created_items
