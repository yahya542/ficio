from rest_framework import serializers
from .models import Ship, Tangkapan

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ['id', 'ship_name']


class TangkapanSerializer(serializers.ModelSerializer):
    ship_name = serializers.CharField(source='ship.ship_name', read_only=True)

    class Meta:
        model = Tangkapan
        fields = ['id', 'ship', 'ship_name', 'jenis_ikan', 'jumlah', 'lokasi_tangkap']
    
    def get_wpp_name(self, obj):
        wpp_map = {
            571: 'Selat Malaka, Laut Andaman',
            572: 'Samudra Hindia barat Sumatera & Selat Sunda',
            573: 'Samudra Hindia selatan Jawa, Laut Sawu & Timor Barat',
            711: 'Selat Karimata (Laut Natuna & Laut China Selatan)',
            712: 'Laut Jawa',
            713: 'Selat Makassar, Teluk Bone, Laut Flores & Laut Bali',
            714: 'Teluk Tolo & Laut Banda',
            715: 'Teluk Tomini, Laut Maluku, Laut Halmahera, Laut Seram & Teluk Berau',
            716: 'Laut Sulawesi & Utara Pulau Halmahera',
            717: 'Teluk Cenderawasih & Samudera Pasifik',
            718: 'Laut Aru, Arafuru & Timor Timur',
        }
        return wpp_map.get(obj.lokasi_tangkap, 'Unknown WPP')