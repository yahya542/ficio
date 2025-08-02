from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ship, Dataset, Prediction, OptimizationResult, CorrelationAnalysis
from .serializers import ShipSerializer, DatasetSerializer, PredictionSerializer, OptimizationResultSerializer, CorrelationAnalysisSerializer
from .ml_models import ml_engine
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Authentication Views
def login_view(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau password salah!')
    
    return render(request, 'login.html')

def register_view(request):
    """Register view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        ship_name = request.POST.get('ship_name')
        ship_id = request.POST.get('ship_id')
        captain_name = request.POST.get('captain_name')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return render(request, 'register.html')
        
        # Check if ship_id already exists
        if Ship.objects.filter(ship_id=ship_id).exists():
            messages.error(request, 'ID Kapal sudah terdaftar!')
            return render(request, 'register.html')
        
        # Create user
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Create ship
        ship = Ship.objects.create(
            user=user,
            ship_name=ship_name,
            ship_id=ship_id,
            captain_name=captain_name
        )
        
        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('login')
    
    return render(request, 'register.html')

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('login')

# Dashboard Views
@login_required
def dashboard(request):
    """Main dashboard view - user specific"""
    # Get user's ship
    try:
        ship = request.user.ship
    except Ship.DoesNotExist:
        ship = None
    
    # Get statistics for this user/ship
    total_datasets = Dataset.objects.filter(user=request.user).count()
    total_predictions = Prediction.objects.filter(user=request.user).count()
    total_optimizations = OptimizationResult.objects.filter(user=request.user).count()
    total_correlations = CorrelationAnalysis.objects.filter(user=request.user).count()
    
    # Get recent activities for this user/ship
    recent_datasets = Dataset.objects.filter(user=request.user)[:5]
    recent_predictions = Prediction.objects.filter(user=request.user).select_related('dataset')[:5]
    recent_optimizations = OptimizationResult.objects.filter(user=request.user).select_related('dataset')[:5]
    
    context = {
        'ship': ship,
        'total_datasets': total_datasets,
        'total_predictions': total_predictions,
        'total_optimizations': total_optimizations,
        'total_correlations': total_correlations,
        'recent_datasets': recent_datasets,
        'recent_predictions': recent_predictions,
        'recent_optimizations': recent_optimizations,
    }
    return render(request, 'dashboard.html', context)

@login_required
def datasets_view(request):
    """Datasets management view - user specific"""
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'datasets.html', {'datasets': datasets})

@login_required
def predictions_view(request):
    """Predictions management view - user specific"""
    predictions = Prediction.objects.filter(user=request.user).select_related('dataset').order_by('-created_at')
    datasets = Dataset.objects.filter(user=request.user).order_by('name')
    return render(request, 'predictions.html', {'predictions': predictions, 'datasets': datasets})

@login_required
def optimization_view(request):
    """Optimization management view - user specific"""
    optimizations = OptimizationResult.objects.filter(user=request.user).select_related('dataset').order_by('-created_at')
    datasets = Dataset.objects.filter(user=request.user).order_by('name')
    return render(request, 'optimization.html', {'optimizations': optimizations, 'datasets': datasets})

@login_required
def correlation_view(request):
    """Correlation analysis view - user specific"""
    correlations = CorrelationAnalysis.objects.filter(user=request.user).select_related('dataset').order_by('-created_at')
    datasets = Dataset.objects.filter(user=request.user).order_by('name')
    return render(request, 'correlation.html', {'correlations': correlations, 'datasets': datasets})

# API Views (existing)
@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)

class DatasetViewSet(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            datasets = Dataset.objects.filter(user=request.user)
        else:
            datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(user=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatasetDetailView(APIView):
    def get(self, request, dataset_id):
        if request.user.is_authenticated:
            dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)
        else:
            dataset = get_object_or_404(Dataset, id=dataset_id)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    def delete(self, request, dataset_id):
        if request.user.is_authenticated:
            dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)
        else:
            dataset = get_object_or_404(Dataset, id=dataset_id)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PredictionView(APIView):
    def post(self, request):
        try:
            dataset_id = request.data.get('dataset_id')
            models_to_train = request.data.get('models', ['Linear'])
            
            if not dataset_id:
                return Response({'error': 'Dataset ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get dataset (user-specific)
            if request.user.is_authenticated:
                dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)
            else:
                dataset = get_object_or_404(Dataset, id=dataset_id)
            
            # Get the file path
            dataset_file = dataset.file.path
            
            # Run prediction using ML engine
            results = ml_engine.train_and_predict(dataset_id, dataset_file, models_to_train)
            
            # Save predictions to database
            saved_predictions = []
            for model_name, result in results.items():
                prediction = Prediction.objects.create(
                    dataset=dataset,
                    user=request.user if request.user.is_authenticated else None,
                    model_type=model_name,
                    predictions=result['predictions'],
                    actual_values=result['actual_values'],
                    mse=result['mse'],
                    mae=result['mae']
                )
                saved_predictions.append(prediction)
            
            return Response({
                'message': f'Successfully ran predictions for {len(saved_predictions)} models',
                'predictions_created': len(saved_predictions),
                'models_trained': list(results.keys())
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Error running prediction: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictionListView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            predictions = Prediction.objects.filter(user=request.user)
        else:
            predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

class PredictionDetailView(APIView):
    def get(self, request, prediction_id):
        if request.user.is_authenticated:
            prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
        else:
            prediction = get_object_or_404(Prediction, id=prediction_id)
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data)
    
    def delete(self, request, prediction_id):
        if request.user.is_authenticated:
            prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
        else:
            prediction = get_object_or_404(Prediction, id=prediction_id)
        prediction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OptimizationView(APIView):
    def post(self, request):
        # Implementation for optimization
        return Response({'message': 'Optimization endpoint'}, status=status.HTTP_200_OK)

class OptimizationListView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            optimizations = OptimizationResult.objects.filter(user=request.user)
        else:
            optimizations = OptimizationResult.objects.all()
        serializer = OptimizationResultSerializer(optimizations, many=True)
        return Response(serializer.data)

class CorrelationView(APIView):
    def post(self, request):
        # Implementation for correlation analysis
        return Response({'message': 'Correlation endpoint'}, status=status.HTTP_200_OK)

class CorrelationListView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            correlations = CorrelationAnalysis.objects.filter(user=request.user)
        else:
            correlations = CorrelationAnalysis.objects.all()
        serializer = CorrelationAnalysisSerializer(correlations, many=True)
        return Response(serializer.data)

class ExportView(APIView):
    def get(self, request, prediction_id):
        if request.user.is_authenticated:
            prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
        else:
            prediction = get_object_or_404(Prediction, id=prediction_id)
        # Implementation for export
        return Response({'message': 'Export endpoint'}, status=status.HTTP_200_OK)
