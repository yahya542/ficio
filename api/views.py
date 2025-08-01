from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Dataset, Prediction, OptimizationResult, CorrelationAnalysis
from .serializers import DatasetSerializer, PredictionSerializer, OptimizationResultSerializer, CorrelationAnalysisSerializer
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Dashboard Views
def dashboard(request):
    """Main dashboard view"""
    # Get statistics
    total_datasets = Dataset.objects.count()
    total_predictions = Prediction.objects.count()
    total_optimizations = OptimizationResult.objects.count()
    total_correlations = CorrelationAnalysis.objects.count()
    
    # Get recent activities
    recent_datasets = Dataset.objects.all()[:5]
    recent_predictions = Prediction.objects.select_related('dataset').all()[:5]
    recent_optimizations = OptimizationResult.objects.select_related('dataset').all()[:5]
    
    context = {
        'total_datasets': total_datasets,
        'total_predictions': total_predictions,
        'total_optimizations': total_optimizations,
        'total_correlations': total_correlations,
        'recent_datasets': recent_datasets,
        'recent_predictions': recent_predictions,
        'recent_optimizations': recent_optimizations,
    }
    return render(request, 'dashboard.html', context)

def datasets_view(request):
    """Datasets management view"""
    datasets = Dataset.objects.all().order_by('-uploaded_at')
    return render(request, 'datasets.html', {'datasets': datasets})

def predictions_view(request):
    """Predictions management view"""
    predictions = Prediction.objects.select_related('dataset').all().order_by('-created_at')
    datasets = Dataset.objects.all().order_by('name')
    return render(request, 'predictions.html', {'predictions': predictions, 'datasets': datasets})

def optimization_view(request):
    """Optimization management view"""
    optimizations = OptimizationResult.objects.select_related('dataset').all().order_by('-created_at')
    datasets = Dataset.objects.all().order_by('name')
    return render(request, 'optimization.html', {'optimizations': optimizations, 'datasets': datasets})

def correlation_view(request):
    """Correlation analysis view"""
    correlations = CorrelationAnalysis.objects.select_related('dataset').all().order_by('-created_at')
    datasets = Dataset.objects.all().order_by('name')
    return render(request, 'correlation.html', {'correlations': correlations, 'datasets': datasets})

# API Views (existing)
@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)

class DatasetViewSet(APIView):
    def get(self, request):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatasetDetailView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    def delete(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PredictionView(APIView):
    def post(self, request):
        # Implementation for prediction
        return Response({'message': 'Prediction endpoint'}, status=status.HTTP_200_OK)

class PredictionListView(APIView):
    def get(self, request):
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

class OptimizationView(APIView):
    def post(self, request):
        # Implementation for optimization
        return Response({'message': 'Optimization endpoint'}, status=status.HTTP_200_OK)

class OptimizationListView(APIView):
    def get(self, request):
        optimizations = OptimizationResult.objects.all()
        serializer = OptimizationResultSerializer(optimizations, many=True)
        return Response(serializer.data)

class CorrelationView(APIView):
    def post(self, request):
        # Implementation for correlation analysis
        return Response({'message': 'Correlation endpoint'}, status=status.HTTP_200_OK)

class CorrelationListView(APIView):
    def get(self, request):
        correlations = CorrelationAnalysis.objects.all()
        serializer = CorrelationAnalysisSerializer(correlations, many=True)
        return Response(serializer.data)

class ExportView(APIView):
    def get(self, request, prediction_id):
        prediction = get_object_or_404(Prediction, id=prediction_id)
        # Implementation for export
        return Response({'message': 'Export endpoint'}, status=status.HTTP_200_OK)
