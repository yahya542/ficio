from django.db import models
from django.utils import timezone
import json

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_data = models.JSONField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-uploaded_at']

class Prediction(models.Model):
    MODEL_CHOICES = [
        ('GRU', 'GRU'),
        ('LSTM', 'LSTM'),
        ('BiLSTM', 'BiLSTM'),
        ('Linear', 'Linear Regression'),
        ('RNN', 'RNN'),
    ]
    
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='predictions')
    model_type = models.CharField(max_length=20, choices=MODEL_CHOICES)
    predictions = models.JSONField()  # Store predictions as JSON
    actual_values = models.JSONField()  # Store actual values as JSON
    mse = models.FloatField()
    mae = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.model_type} - {self.dataset.name}"
    
    class Meta:
        ordering = ['-created_at']

class OptimizationResult(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='optimization_results')
    solutions = models.JSONField()  # Store all solutions
    best_solution = models.JSONField()  # Store best solution
    best_total_stok = models.FloatField()
    best_mse = models.FloatField()
    population_size = models.IntegerField(default=40)
    generations = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"NSGA-III - {self.dataset.name}"
    
    class Meta:
        ordering = ['-created_at']

class CorrelationAnalysis(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='correlation_analyses')
    correlation_matrix = models.JSONField()  # Store correlation matrix as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Correlation - {self.dataset.name}"
    
    class Meta:
        ordering = ['-created_at']
