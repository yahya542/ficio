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


# Serializer untuk Register
from rest_framework import serializers
from ..models import CustomUser, Kapal, Profile, WPP

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('pemilik_kapal', 'Pemilik Kapal'), ('nahkoda', 'Nahkoda')])
    
    # Pemilik kapal
    no_buku_kapal = serializers.CharField(write_only=True, required=False)
    nama_kapal = serializers.CharField(write_only=True, required=False)
    wpp_code = serializers.CharField(write_only=True, required=False)

    # Nahkoda
    no_reg_bkp = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'role',
            'no_buku_kapal', 'nama_kapal', 'wpp_code',  # untuk pemilik kapal
            'no_reg_bkp'  # untuk nahkoda
        ]

    def validate(self, attrs):
        role = attrs.get('role')
        if role == 'pemilik_kapal':
            if not attrs.get('nama_kapal') or not attrs.get('no_buku_kapal') or not attrs.get('wpp_code'):
                raise serializers.ValidationError("Pemilik kapal wajib isi nama_kapal, no_buku_kapal, dan wpp_code")
            if not WPP.objects.filter(code=attrs['wpp_code']).exists():
                raise serializers.ValidationError("WPP code tidak ditemukan")
        elif role == 'nahkoda':
            if not attrs.get('no_reg_bkp'):
                raise serializers.ValidationError("Nahkoda wajib isi no_reg_bkp dari kapal yang sudah ada")
            if not Kapal.objects.filter(no_reg_bkp=attrs['no_reg_bkp']).exists():
                raise serializers.ValidationError("Kapal dengan no_reg_bkp tersebut tidak ditemukan")
        return attrs

    def generate_no_reg_bkp(self, wpp_code, no_buku_kapal):
        total_existing = Kapal.objects.count()
        last2 = no_buku_kapal[-2:] if len(no_buku_kapal) >= 2 else no_buku_kapal.zfill(2)
        cascading = str(total_existing + 1).zfill(3)
        return f"REG{wpp_code}{last2}{cascading}"

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.get('username')

        # Buat user
        user = CustomUser(username=username, email=email, role=role)
        user.set_password(password)
        user.save()

        # Buat kapal/profile sesuai role
        if role == 'pemilik_kapal':
            nama_kapal = validated_data.pop('nama_kapal')
            no_buku_kapal = validated_data.pop('no_buku_kapal')
            wpp_code = validated_data.pop('wpp_code')

            no_reg_bkp = self.generate_no_reg_bkp(wpp_code, no_buku_kapal)
            kapal = Kapal.objects.create(
                nama_kapal=nama_kapal,
                no_buku_kapal=no_buku_kapal,
                no_reg_bkp=no_reg_bkp
            )

        else:  # nahkoda
            no_reg_bkp = validated_data.pop('no_reg_bkp')
            kapal = Kapal.objects.get(no_reg_bkp=no_reg_bkp)

        Profile.objects.create(user=user, kapal=kapal, role=role)
        return user
