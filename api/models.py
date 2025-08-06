from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json

# Kapal Model
class Ship(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ship')
    ship_name = models.CharField(max_length=255)
    ship_id = models.CharField(max_length=50, unique=True)
    captain_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ship_type = models.CharField(max_length=100, blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    home_port = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ship_name} ({self.ship_id})"

    class Meta:
        ordering = ['-created_at']

# Dataset Model
class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_data = models.JSONField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='datasets', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-uploaded_at']

# Prediction Model
class Prediction(models.Model):
    MODEL_CHOICES = [
        ('GRU', 'GRU'),
        ('LSTM', 'LSTM'),
        ('BiLSTM', 'BiLSTM'),
        ('Linear', 'Linear Regression'),
        ('RNN', 'RNN'),
    ]

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='predictions')
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    model_type = models.CharField(max_length=20, choices=MODEL_CHOICES)
    predictions = models.JSONField()
    actual_values = models.JSONField()
    mse = models.FloatField()
    mae = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_type} - {self.dataset.name}"

    class Meta:
        ordering = ['-created_at']

# Optimization Result Model
class OptimizationResult(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='optimization_results')
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='optimization_results', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='optimization_results', null=True, blank=True)
    solutions = models.JSONField()
    best_solution = models.JSONField()
    best_total_stok = models.FloatField()
    best_mse = models.FloatField()
    population_size = models.IntegerField(default=40)
    generations = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NSGA-III - {self.dataset.name}"

    class Meta:
        ordering = ['-created_at']

# Correlation Analysis Model
class CorrelationAnalysis(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='correlation_analyses')
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, related_name='correlation_analyses', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='correlation_analyses', null=True, blank=True)
    correlation_matrix = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correlation - {self.dataset.name}"

    class Meta:
        ordering = ['-created_at']

# Realisasi Model
class Realisasi(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='realisasi/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

# Kuota Model
class Kuota(models.Model):
    jenis_ikan = models.CharField(max_length=100)
    total_kuota = models.IntegerField()
    kuota_terpakai = models.IntegerField(default=0)

    @property
    def sisa_kuota(self):
        return self.total_kuota - self.kuota_terpakai

    def __str__(self):
        return f"{self.jenis_ikan} - Sisa Kuota: {self.sisa_kuota}"

# Pelabuhan Model
class Pelabuhan(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

# Ikan Model (Tangkapan)
class Ikan(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    jenis_ikan = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    lokasi_tangkap = models.CharField(max_length=100)
    tanggal_input = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Optional logic for kuota check
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jenis_ikan} - {self.ship.ship_name}"
