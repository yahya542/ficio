from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import CustomUser, Kapal, Profile
from rest_framework import serializers
from ..models import CustomUser, Kapal, Profile, WPP






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


class RegisterSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('pemilik_kapal', 'Pemilik Kapal'),
        ('nahkoda', 'Nahkoda'),
        ('auditori', 'Auditori'),
        ('regulator', 'Regulator'),
    ]

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    
    # hanya wajib untuk role kapal
    no_buku_kapal = serializers.CharField(write_only=True, required=False)
    nama_kapal = serializers.CharField(write_only=True, required=False)
    wpp_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'no_buku_kapal', 'nama_kapal', 'wpp_code']

    def validate(self, attrs):
        role = attrs.get('role')
        no_buku_kapal = attrs.get('no_buku_kapal')

        if role in ['pemilik_kapal', 'nahkoda']:
            if not no_buku_kapal:
                raise serializers.ValidationError({
                    "no_buku_kapal": "Field wajib untuk role pemilik_kapal / nahkoda"
                })
            try:
                kapal = Kapal.objects.get(no_buku_kapal=no_buku_kapal)
            except Kapal.DoesNotExist:
                raise serializers.ValidationError(f"Kapal dengan no_buku_kapal {no_buku_kapal} tidak ditemukan")
            attrs['kapal_instance'] = kapal

            if role == 'pemilik_kapal':
                if not attrs.get('nama_kapal') or not attrs.get('wpp_code'):
                    raise serializers.ValidationError("Pemilik kapal wajib isi nama_kapal dan wpp_code")
                if not WPP.objects.filter(code=attrs['wpp_code']).exists():
                    raise serializers.ValidationError("WPP code tidak ditemukan")

        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.get('username')

        kapal = validated_data.pop('kapal_instance', None)

        user = CustomUser(username=username, email=email, role=role)
        user.set_password(password)
        user.save()

        # buat profile jika role terkait kapal
        if kapal:
            Profile.objects.create(user=user, kapal=kapal, role=role)

        return user