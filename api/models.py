from django.db import models
from django.contrib.auth.models import User

class Ship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ship_name = models.CharField(max_length=100)

    def __str__(self):
        return self.ship_name

class Tangkapan(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    jenis_ikan = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    lokasi_tangkap = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.jenis_ikan} - {self.ship.ship_name}"
