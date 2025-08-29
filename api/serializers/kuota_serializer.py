from rest_framework import serializers
from ..models import Kapal
from rest_framework.serializers import Serializer, CharField, FloatField, ValidationError
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes


class KuotaKapalSerializer(serializers.ModelSerializer):
    no_buku_kapal = serializers.CharField(source='kapal.no_buku_kapal', read_only=True)
    sisa_kuota = serializers.SerializerMethodField()

    class Meta:
        model = Kapal
        fields = ['id', 'kapal', 'no_buku_kapal', 'kuota', 'kuota_terpakai', 'sisa_kuota']
        read_only_fields = ['kuota_terpakai', 'sisa_kuota']

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_sisa_kuota(self, obj):
        # sisa kuota = kuota yang dialokasikan - kuota terpakai
        return obj.kuota - obj.kuota_terpakai

class KuotaKapalInputSerializer(Serializer):
    no_buku_kapal = CharField(help_text="Ship registration number")
    kuota = FloatField(min_value=0, help_text="Allocated quota in kilograms")

    def validate_no_buku_kapal(self, value):
        if not Kapal.objects.filter(no_buku_kapal=value).exists():
            raise ValidationError("Kapal tidak ditemukan")
        return value

    def create(self, validated_data):
        kapal = Kapal.objects.get(no_buku_kapal=validated_data['no_buku_kapal'])
        kuota, _ = Kapal.objects.update_or_create(
            kapal=kapal,
            defaults={'kuota': validated_data['kuota']}
        )
        return kuota