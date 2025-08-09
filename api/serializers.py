from rest_framework import serializers
from .models import Ship, Tangkapan
from .models import Ikan, WPP

#kapal serializers
class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'ship_name']

class ShipIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id']

class ShipDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')  # ambil nama user dari ForeignKey

    class Meta:
        model = Ship
        fields = ['id', 'ship_name', 'user']

#ikan serializers
class IkanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ikan
        fields = ['id', 'nama']

#tangkapan serializers
class TangkapanSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship.ship_name', read_only=True)
    wpp_name = serializers.CharField(source='lokasi.name', read_only=True)  # ambil nama dari model WPP
    ship_id = serializers.IntegerField(write_only=True)
    lokasi = serializers.IntegerField(write_only=True)  # input kode WPP (misal: 713)
    id_ikan = serializers.IntegerField(write_only=True)
    jenis_ikan = serializers.CharField(source='jenis_ikan.nama', read_only=True)
 

    class Meta:
        model = Tangkapan
        fields = ['ship_id', 'jenis_ikan', 'id_ikan','jumlah', 'lokasi', 'ship_name', 'wpp_name']

    def create(self, validated_data):
        ship_id = validated_data.pop('ship_id')
        lokasi_code = validated_data.pop('lokasi')
        id_ikan = validated_data.pop('id_ikan')

        try:
            ship = Ship.objects.get(id=ship_id)
        except Ship.DoesNotExist:
            raise serializers.ValidationError("Ship with given ID does not exist.")

        try:
            wpp = WPP.objects.get(code=lokasi_code)
        except WPP.DoesNotExist:
            raise serializers.ValidationError("WPP with given code does not exist.")

        try:
            ikan = Ikan.objects.get(id=id_ikan)
        except Ikan.DoesNotExist:
            raise serializers.ValidationError("Ikan with given ID does not exist.")

        return Tangkapan.objects.create(
            ship=ship,
            lokasi=wpp,
            jenis_ikan=ikan,
            **validated_data
        )
