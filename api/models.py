from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

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


class Kapal(models.Model):
    no_reg_bkp = models.CharField(max_length=15, unique=True)  # cukup panjang untuk format REG + kode
    no_buku_kapal = models.CharField(max_length=50, blank=True, null=True)
    nama_kapal = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.no_reg_bkp} - {self.nama_kapal}"



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


# Model lain tetap sama
class Ikan(models.Model):
    nama_ikan = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nama_ikan

class JenisIkan(models.Model):
    nama_ikan= models.CharField(max_length=100)
    def __str__(self):
        return self.nama_ikan

class WPP(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.code} - {self.name}"

class TangkapanIkan(models.Model):
    kapal = models.ForeignKey(Kapal, on_delete=models.CASCADE, related_name="catches")
    jenis_ikan = models.ForeignKey(JenisIkan, on_delete=models.CASCADE, related_name="catches")
    weight = models.FloatField(help_text="Berat dalam kilogram")
    location = models.ForeignKey(WPP, on_delete=models.CASCADE, related_name="catches")
    def __str__(self):
        return f"{self.jenis_ikan.name} - {self.kapal.nama_kapal} ({self.weight} kg)"
