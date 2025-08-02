from django.contrib import admin
from .models import Ship, Dataset, Prediction, OptimizationResult, CorrelationAnalysis

@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
    list_display = ['ship_name', 'ship_id', 'captain_name', 'user', 'home_port', 'created_at']
    list_filter = ['created_at', 'ship_type', 'home_port']
    search_fields = ['ship_name', 'ship_id', 'captain_name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'ship', 'user', 'uploaded_at', 'description']
    list_filter = ['uploaded_at', 'ship']
    search_fields = ['name', 'description', 'ship__ship_name']
    readonly_fields = ['uploaded_at']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['model_type', 'dataset', 'ship', 'mse', 'mae', 'created_at']
    list_filter = ['model_type', 'created_at', 'dataset', 'ship']
    search_fields = ['model_type', 'dataset__name', 'ship__ship_name']
    readonly_fields = ['created_at']

@admin.register(OptimizationResult)
class OptimizationResultAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'ship', 'best_total_stok', 'best_mse', 'population_size', 'generations', 'created_at']
    list_filter = ['created_at', 'dataset', 'ship']
    search_fields = ['dataset__name', 'ship__ship_name']
    readonly_fields = ['created_at']

@admin.register(CorrelationAnalysis)
class CorrelationAnalysisAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'ship', 'created_at']
    list_filter = ['created_at', 'dataset', 'ship']
    search_fields = ['dataset__name', 'ship__ship_name']
    readonly_fields = ['created_at']
