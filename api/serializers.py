from rest_framework import serializers
from .models import Dataset, Prediction, OptimizationResult, CorrelationAnalysis

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'file', 'uploaded_at', 'processed_data', 'description']
        read_only_fields = ['id', 'uploaded_at', 'processed_data']

class PredictionSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source='dataset.name', read_only=True)
    
    class Meta:
        model = Prediction
        fields = ['id', 'dataset', 'dataset_name', 'model_type', 'predictions', 'actual_values', 'mse', 'mae', 'created_at']
        read_only_fields = ['id', 'created_at']

class OptimizationResultSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source='dataset.name', read_only=True)
    
    class Meta:
        model = OptimizationResult
        fields = ['id', 'dataset', 'dataset_name', 'solutions', 'best_solution', 'best_total_stok', 'best_mse', 'population_size', 'generations', 'created_at']
        read_only_fields = ['id', 'created_at']

class CorrelationAnalysisSerializer(serializers.ModelSerializer):
    dataset_name = serializers.CharField(source='dataset.name', read_only=True)
    
    class Meta:
        model = CorrelationAnalysis
        fields = ['id', 'dataset', 'dataset_name', 'correlation_matrix', 'created_at']
        read_only_fields = ['id', 'created_at']

class PredictionRequestSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()
    models = serializers.ListField(
        child=serializers.CharField(),
        default=['GRU', 'LSTM', 'BiLSTM', 'Linear']
    )

class OptimizationRequestSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField()
    population_size = serializers.IntegerField(default=40)
    generations = serializers.IntegerField(default=100)

class CorrelationRequestSerializer(serializers.Serializer):
    dataset_id = serializers.IntegerField() 