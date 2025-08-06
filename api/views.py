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
from .models import Ship, Dataset, Prediction, OptimizationResult, CorrelationAnalysis, Realisasi, Kuota, Ikan
from .serializers import ShipSerializer, DatasetSerializer, PredictionSerializer, OptimizationResultSerializer, CorrelationAnalysisSerializer, RealisasiSerializer
from django.views import View
import pandas as pd
from django.contrib.auth.decorators import login_required, user_passes_test


# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.username}!')
            return redirect('user_dashboard' if not user.is_staff else 'admin_dashboard')
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
def user_dashboard(request):
    ship = getattr(request.user, 'ship', None)
    tangkapan = Ikan.objects.filter(ship=ship)
    kuotas = Kuota.objects.all()

    context = {
        'ship': ship,
        'tangkapan': tangkapan,
        'kuotas': kuotas
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def admin_dashboard(request):
    ships = Ship.objects.all()
    kuotas = Kuota.objects.all()

    if request.method == 'POST':
        if 'add_tangkapan' in request.POST:
            ship_id = request.POST.get('ship_id')
            jenis_ikan = request.POST.get('jenis_ikan')
            jumlah = request.POST.get('jumlah')
            lokasi_tangkap = request.POST.get('lokasi_tangkap')

            ship = get_object_or_404(Ship, id=ship_id)
            Ikan.objects.create(ship=ship, jenis_ikan=jenis_ikan, jumlah=jumlah, lokasi_tangkap=lokasi_tangkap)
            messages.success(request, 'Data tangkapan berhasil ditambahkan!')

        if 'add_kuota' in request.POST:
            jenis_ikan = request.POST.get('jenis_ikan')
            total_kuota = request.POST.get('total_kuota')

            Kuota.objects.create(jenis_ikan=jenis_ikan, total_kuota=total_kuota)
            messages.success(request, 'Kuota berhasil ditambahkan!')

        return redirect('admin_dashboard')

    context = {
        'ships': ships,
        'kuotas': kuotas
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def dashboard(request):
    if request.user.is_staff:
        # Admin Dashboard
        ships = Ship.objects.all()
        kuotas = Kuota.objects.all()

        if request.method == 'POST':
            if 'add_tangkapan' in request.POST:
                ship_id = request.POST.get('ship_id')
                jenis_ikan = request.POST.get('jenis_ikan')
                jumlah = request.POST.get('jumlah')
                lokasi_tangkap = request.POST.get('lokasi_tangkap')

                ship = get_object_or_404(Ship, id=ship_id)
                Ikan.objects.create(ship=ship, jenis_ikan=jenis_ikan, jumlah=jumlah, lokasi_tangkap=lokasi_tangkap)
                messages.success(request, 'Data tangkapan berhasil ditambahkan!')

            if 'add_kuota' in request.POST:
                jenis_ikan = request.POST.get('jenis_ikan')
                total_kuota = request.POST.get('total_kuota')

                Kuota.objects.create(jenis_ikan=jenis_ikan, total_kuota=total_kuota)
                messages.success(request, 'Kuota berhasil ditambahkan!')

            return redirect('dashboard')

        context = {
            'ships': ships,
            'kuotas': kuotas
        }
        return render(request, 'admin/dashboard.html', context)

    else:
        # User Dashboard
        ship = getattr(request.user, 'ship', None)
        tangkapan = Ikan.objects.filter(ship=ship)
        kuotas = Kuota.objects.all()

        context = {
            'ship': ship,
            'tangkapan': tangkapan,
            'kuotas': kuotas
        }
        return render(request, 'user/dashboard.html', context)
@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'}, status=status.HTTP_200_OK)

# Remaining APIViews and Views will stay unchanged and used for API interactions as needed.
#admin 
def admin_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))

@admin_required
def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, 'admin/dataset_list.html', {'datasets': datasets})

@admin_required
def run_prediction(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dataset_file_path = os.path.join('media', dataset.file.name)

    results = ml_engine.train_and_predict(dataset_id, dataset_file_path)

    # Save Prediction Results (Optional, here just show it in frontend)
    return render(request, 'admin/prediction_result.html', {
        'dataset': dataset,
        'results': results
    })

@admin_required
def correlation_analysis(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dataset_file_path = os.path.join('media', dataset.file.name)

    correlation_data = ml_engine.get_correlation_analysis(dataset_file_path)

    return render(request, 'admin/correlation_result.html', {
        'dataset': dataset,
        'correlation': correlation_data
    })

@admin_required
def run_optimization(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dataset_file_path = os.path.join('media', dataset.file.name)

    optimization_data = ml_engine.run_optimization(dataset_file_path)

    return render(request, 'admin/optimization_result.html', {
        'dataset': dataset,
        'optimization': optimization_data
    })

