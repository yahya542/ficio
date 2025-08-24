from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone



# =========================
# CUSTOM USER MANAGER 
# =========================
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role='user', **extra_fields):
        if not username:
            raise ValueError('Username harus diisi')
        email = extra_fields.get('email')
        if not email:
            raise ValueError('Email harus diisi')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, role='admin', **extra_fields)



# =========================
# CUSTOM USER MODEL
# =========================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, default='user')  # role umum: admin/user
    email = models.EmailField(unique=True, blank=True, null=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



# =========================
# KAPAL
# =========================
class Kapal(models.Model):
    no_buku_kapal = models.CharField(max_length=50, unique=True)  # wajib & unik
    nama_kapal = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.no_buku_kapal} - {self.nama_kapal}"




# =========================
# PROFILE USER 
# =========================
class Profile(models.Model):
    ROLE_CHOICES = [
        ('nahkoda', 'Nahkoda'),
        ('pemilik_kapal', 'Pemilik Kapal'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    kapal = models.ForeignKey(Kapal, on_delete=models.CASCADE, related_name='profiles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('kapal', 'role')

    def __str__(self):
        return f"{self.user.username} ({self.role})"




# =========================
# NAMA IKAN DAN JENIS IKAN 
# =========================

class JenisIkan(models.Model):
    nama = models.CharField(max_length=100, unique=True)  # Nama jenis ikan unik

    def __str__(self):
        return self.nama
class Ikan(models.Model):
    nama_ikan = models.CharField(max_length=150)
    jenis_ikan = models.ForeignKey(
        JenisIkan,
        on_delete=models.CASCADE,  # Kalau jenis ikan dihapus, semua ikan terkait ikut terhapus
        related_name='daftar_ikan'
    )

    def __str__(self):
        return f"{self.nama_ikan} ({self.jenis_ikan.nama})"


# =========================
# LOKASI WPP 
# =========================
class WPP(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.code} - {self.name}"


# =========================
# KUOTA PER KAPAL
# =========================
class KuotaKapal(models.Model):
    kapal = models.ForeignKey("Kapal", on_delete=models.CASCADE, related_name="alokasi_kuota")
    kuota = models.FloatField(help_text="Total kuota kapal (kg/ton)")
    kuota_terpakai = models.FloatField(default=0, help_text="Kuota yang sudah dipakai (kg/ton)")

    class Meta:
        unique_together = ("kapal",)

    def __str__(self):
        return f"{self.kapal.nama_kapal} - {self.kuota}kg"

    @property
    def sisa_kuota(self):
        return self.kuota - self.kuota_terpakai


# =========================
# TANGKAPAN IKAN
# =========================
class TangkapanIkan(models.Model):
    kapal = models.ForeignKey(Kapal, to_field="no_buku_kapal", on_delete=models.CASCADE, related_name="catches")
    jenis_ikan = models.ForeignKey(
        JenisIkan,
        on_delete=models.CASCADE,
        default=1  # pakai id Tuna yang sudah ada
    )
    weight = models.FloatField(help_text="Berat dalam kilogram")
    location = models.ForeignKey(WPP, on_delete=models.CASCADE, related_name="catches")
    created_at = models.DateTimeField(default=timezone.now)
   

    # relasi baru ke Kuota
    kuota = models.ForeignKey(
        KuotaKapal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="penangkapan"
    )
