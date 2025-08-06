from rest_framework import serializers
from .models import Ship, Dataset, Prediction, OptimizationResult, CorrelationAnalysis, Realisasi

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = '__all__'

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class OptimizationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizationResult
        fields = '__all__'

class CorrelationAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrelationAnalysis
        fields = '__all__'

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

class RealisasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realisasi
        fields = '__all__'
    
    def validate_file(self, value):
        max_size = 50 * 1024 * 1024  # 10 MB
        if value.size > max_size:
            raise serializers.ValidationError("Ukuran file maksimal 10MB.")
        return value