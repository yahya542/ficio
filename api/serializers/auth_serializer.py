from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import CustomUser, Kapal, Profile


# Serializer untuk Login + Custom Response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Ambil user yang login
        user = self.user

        # Tambahkan data custom di response token
        data.update({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.profile.role if hasattr(user, "profile") else None
            }
        })

        return data

from rest_framework import serializers
from ..models import CustomUser, Kapal, Profile, WPP

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('pemilik_kapal', 'Pemilik Kapal'), ('nahkoda', 'Nahkoda')])
    
    # Semua role pakai no_buku_kapal
    no_buku_kapal = serializers.CharField(write_only=True, required=True)
    nama_kapal = serializers.CharField(write_only=True, required=False)  # hanya untuk pemilik kapal
    wpp_code = serializers.CharField(write_only=True, required=False)   # hanya untuk pemilik kapal

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'no_buku_kapal', 'nama_kapal', 'wpp_code']

    def validate(self, attrs):
        role = attrs.get('role')
        no_buku_kapal = attrs.get('no_buku_kapal')

        # Pastikan kapal sudah ada
        try:
            kapal = Kapal.objects.get(no_buku_kapal=no_buku_kapal)
        except Kapal.DoesNotExist:
            raise serializers.ValidationError(f"Kapal dengan no_buku_kapal {no_buku_kapal} tidak ditemukan")

        # Untuk pemilik kapal, cek wajib isi nama_kapal dan wpp_code
        if role == 'pemilik_kapal':
            if not attrs.get('nama_kapal') or not attrs.get('wpp_code'):
                raise serializers.ValidationError("Pemilik kapal wajib isi nama_kapal dan wpp_code")
            if not WPP.objects.filter(code=attrs['wpp_code']).exists():
                raise serializers.ValidationError("WPP code tidak ditemukan")

        attrs['kapal_instance'] = kapal  # simpan instance kapal untuk create
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.get('username')
        kapal = validated_data.pop('kapal_instance')

        # Buat user
        user = CustomUser(username=username, email=email, role=role)
        user.set_password(password)
        user.save()

        # Buat profile
        Profile.objects.create(user=user, kapal=kapal, role=role)
        return user
