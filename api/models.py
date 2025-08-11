from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, noreg_bkp, password=None, role='user', **extra_fields):
        if not noreg_bkp:
            raise ValueError('noreg_bkp harus diisi')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(noreg_bkp=noreg_bkp, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, noreg_bkp, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # superuser biasanya admin
        return self.create_user(noreg_bkp, password, role='admin', **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    noreg_bkp = models.CharField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, default='user')  

    objects = CustomUserManager()
    USERNAME_FIELD = 'noreg_bkp'

    def __str__(self):
        return self.noreg_bkp


class Kapal(models.Model):
    nama_kapal = models.CharField(max_length=100)
    pemilik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kapal_dimiliki')
    nahkoda = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='kapal_dinahkodai')

    def __str__(self):
        return self.nama_kapal


class JenisIkan(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

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

