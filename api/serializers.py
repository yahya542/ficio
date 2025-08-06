from rest_framework import serializers
from .models import Ship, Ikan

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'ship_name', 'ship_id', 'captain_name']

class IkanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ikan
        fields = ['id', 'jenis_ikan', 'jumlah', 'lokasi_tangkap', 'ship']
