from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Ship, Dataset, Prediction, OptimizationResult, CorrelationAnalysis, Realisasi
from .serializers import ShipSerializer, DatasetSerializer, PredictionSerializer, OptimizationResultSerializer, CorrelationAnalysisSerializer, RealisasiSerializer
from .ml_models import ml_engine
import pandas as pd




# Authentication Views
def login_view(request):
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        ship_name = request.POST.get('ship_name')
        ship_id = request.POST.get('ship_id')
        captain_name = request.POST.get('captain_name')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return render(request, 'register.html')
        
        if Ship.objects.filter(ship_id=ship_id).exists():
            messages.error(request, 'ID Kapal sudah terdaftar!')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        Ship.objects.create(user=user, ship_name=ship_name, ship_id=ship_id, captain_name=captain_name)
        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('login')

@login_required
def dashboard(request):
    try:
        ship = request.user.ship
    except Ship.DoesNotExist:
        ship = None
    
    context = {
        'ship': ship,
        'total_datasets': Dataset.objects.filter(user=request.user).count(),
        'total_predictions': Prediction.objects.filter(user=request.user).count(),
        'total_optimizations': OptimizationResult.objects.filter(user=request.user).count(),
        'total_correlations': CorrelationAnalysis.objects.filter(user=request.user).count(),
        'recent_datasets': Dataset.objects.filter(user=request.user)[:5],
        'recent_predictions': Prediction.objects.filter(user=request.user)[:5],
        'recent_optimizations': OptimizationResult.objects.filter(user=request.user)[:5],
    }
    return render(request, 'dashboard.html', context)

@login_required
def datasets_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        description = request.POST.get('description', '')
        
        if name and file:
            if not file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return redirect('datasets')
            
            Dataset.objects.create(name=name, file=file, description=description, user=request.user)
            messages.success(request, f'Dataset "{name}" uploaded successfully!')
            return redirect('datasets')
        else:
            messages.error(request, 'Please provide a name and file.')
    datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'datasets.html', {'datasets': datasets})

@login_required
def predictions_view(request):
    predictions = Prediction.objects.filter(user=request.user).select_related('dataset').order_by('-created_at')
    datasets = Dataset.objects.filter(user=request.user).order_by('name')
    return render(request, 'predictions.html', {'predictions': predictions, 'datasets': datasets})

@login_required
def optimization_view(request):
    optimizations = OptimizationResult.objects.filter(user=request.user).select_related('dataset').order_by('-created_at')
    datasets = Dataset.objects.filter(user=request.user).order_by('name')
    return render(request, 'optimization.html', {'optimizations': optimizations, 'datasets': datasets})

@login_required
def correlation_view(request):
    correlations = CorrelationAnalysis.objects.filter(user=request.user).select_related('dataset').order_by('-created_at')
    datasets = Dataset.objects.filter(user=request.user).order_by('name')
    return render(request, 'correlation.html', {'correlations': correlations, 'datasets': datasets})

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)


@login_required
def realisasi_upload_page(request):
    if request.method == 'POST':
        # FE form handling can call API
        pass
    return render(request, 'realisasi.html')













# --- API CLASS BASED VIEWS (CSRF EXEMPTED) ---
@method_decorator(csrf_exempt, name='dispatch')
class DatasetViewSet(APIView):
    def get(self, request):
        datasets = Dataset.objects.filter(user=request.user) if request.user.is_authenticated else Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            dataset = serializer.save(user=request.user if request.user.is_authenticated else None)
            try: 
                df = pd.read_csv(dataset.file.path)
                datas_real = df.iloc[:, 0]
                sum_data = datas_real.sum()
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                'id': dataset.id,
                'name': dataset.name,
                'file': dataset.file.url,
                'data_real_sum': sum_data  # <-- Total data real
            }, status=status.HTTP_201_CREATED)
            
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class DatasetDetailView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user if request.user.is_authenticated else None)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    def delete(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user if request.user.is_authenticated else None)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_exempt, name='dispatch')
class DatasetPreviewView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user if request.user.is_authenticated else None)
        try:
            df = pd.read_csv(dataset.file.path)
            data = df.head(10).to_dict('records')
            return Response({
                'data': data,
                'total_rows': len(df),
                'columns': list(df.columns),
                'dataset_name': dataset.name
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class DatasetDownloadView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user if request.user.is_authenticated else None)
        try:
            with open(dataset.file.path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{dataset.name}.csv"'
                return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class PredictionView(APIView):
    def post(self, request):
        try:
            dataset_id = request.data.get('dataset_id')
            models_to_train = request.data.get('models', ['Linear'])
            
            if not dataset_id:
                return Response({'error': 'Dataset ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user if request.user.is_authenticated else None)
            dataset_file = dataset.file.path
            
            results = ml_engine.train_and_predict(dataset_id, dataset_file, models_to_train)
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
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class PredictionListView(APIView):
    def get(self, request):
        predictions = Prediction.objects.filter(user=request.user) if request.user.is_authenticated else Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class PredictionDetailView(APIView):
    def get(self, request, prediction_id):
        prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user if request.user.is_authenticated else None)
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data)
    
    def delete(self, request, prediction_id):
        prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user if request.user.is_authenticated else None)
        prediction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_exempt, name='dispatch')
class OptimizationView(APIView):
    def post(self, request):
        return Response({'message': 'Optimization endpoint'}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class OptimizationListView(APIView):
    def get(self, request):
        optimizations = OptimizationResult.objects.filter(user=request.user) if request.user.is_authenticated else OptimizationResult.objects.all()
        serializer = OptimizationResultSerializer(optimizations, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class CorrelationView(APIView):
    def post(self, request):
        return Response({'message': 'Correlation endpoint'}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class CorrelationListView(APIView):
    def get(self, request):
        correlations = CorrelationAnalysis.objects.filter(user=request.user) if request.user.is_authenticated else CorrelationAnalysis.objects.all()
        serializer = CorrelationAnalysisSerializer(correlations, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class ExportView(APIView):
    def get(self, request, prediction_id):
        prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user if request.user.is_authenticated else None)
        return Response({'message': 'Export endpoint'}, status=status.HTTP_200_OK)
#tambahan 
@method_decorator(csrf_exempt, name='dispatch')
class DatasetRealSumView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user if request.user.is_authenticated else None)
        try:
            df = pd.read_csv(dataset.file.path)

            # Hitung total volume_pendaratan
            total_volume = df['volume_pendaratan'].sum()

            # Kalau mau tambah total dari kolom lain (misal stok_ikan):
            total_stok = df['stok_ikan'].sum()

            return Response({
                'dataset_id': dataset.id,
                'dataset_name': dataset.name,
                'total_volume_pendaratan': total_volume,
                'total_stok_ikan': total_stok
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class RealisasiUploadView(APIView):
    def post(self, request):
        serializer = RealisasiSerializer(data=request.data)
        if serializer.is_valid():
            realisasi = serializer.save(user=request.user if request.user.is_authenticated else None)
            try:
                # Load CSV from saved file path
                df = pd.read_csv(realisasi.file.path)

                # Preview first 10 rows
                data_preview = df.head(10).to_dict('records')

                # Calculate Sums
                total_volume_pendaratan = df['volume_pendaratan'].sum() if 'volume_pendaratan' in df.columns else 0
                total_stok_ikan = df['stok_ikan'].sum() if 'stok_ikan' in df.columns else 0

                return Response({
                    'id': realisasi.id,
                    'name': realisasi.name,
                    'file': realisasi.file.url,
                    'data_preview': data_preview,
                    'total_volume_pendaratan': total_volume_pendaratan,
                    'total_stok_ikan': total_stok_ikan,
                    'total_rows': len(df),
                    'columns': list(df.columns),
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class RealisasiListView(APIView):
    def get(self, request):
        realisasi = Realisasi.objects.filter(user=request.user) if request.user.is_authenticated else Realisasi.objects.all()
        serializer = RealisasiSerializer(realisasi, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class RealisasiDetailView(APIView):
    def get(self, request, realisasi_id):
        realisasi = get_object_or_404(Realisasi, id=realisasi_id, user=request.user if request.user.is_authenticated else None)
        serializer = RealisasiSerializer(realisasi)
        return Response(serializer.data)
@method_decorator(csrf_exempt, name='dispatch')
class RealisasiSumView(APIView):
    def get(self, request, realisasi_id):
        realisasi = get_object_or_404(Realisasi, id=realisasi_id, user=request.user if request.user.is_authenticated else None)
        try:
            df = pd.read_csv(realisasi.file.path)

            total_volume = df['volume_pendaratan'].sum() if 'volume_pendaratan' in df.columns else 0
            total_stok = df['stok_ikan'].sum() if 'stok_ikan' in df.columns else 0

            return Response({
                'realisasi_id': realisasi.id,
                'realisasi_name': realisasi.name,
                'total_volume_pendaratan': total_volume,
                'total_stok_ikan': total_stok
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class RealisasiPreviewView(APIView):
    def get(self, request, realisasi_id):
        realisasi = get_object_or_404(Realisasi, id=realisasi_id, user=request.user if request.user.is_authenticated else None)
        try:
            df = pd.read_csv(realisasi.file.path)
            data_preview = df.head(10).to_dict('records')
            total_volume_pendaratan = df['volume_pendaratan'].sum() if 'volume_pendaratan' in df.columns else 0
            total_stok_ikan = df['stok_ikan'].sum() if 'stok_ikan' in df.columns else 0

            return Response({
                'data_preview': data_preview,
                'total_volume_pendaratan': total_volume_pendaratan,
                'total_stok_ikan': total_stok_ikan
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

