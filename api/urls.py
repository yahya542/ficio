from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Dataset endpoints
    path('datasets/', views.DatasetViewSet.as_view(), name='dataset-list'),
    path('datasets/<int:dataset_id>/', views.DatasetDetailView.as_view(), name='dataset-detail'),
    
    # Prediction endpoints
    path('predict/', views.PredictionView.as_view(), name='predict'),
    path('predictions/', views.PredictionListView.as_view(), name='prediction-list'),
    
    # Optimization endpoints
    path('optimize/', views.OptimizationView.as_view(), name='optimize'),
    path('optimization-results/', views.OptimizationListView.as_view(), name='optimization-list'),
    
    # Correlation endpoints
    path('correlation/', views.CorrelationView.as_view(), name='correlation'),
    path('correlation-results/', views.CorrelationListView.as_view(), name='correlation-list'),
    
    # Export endpoint
    path('export/<int:prediction_id>/', views.ExportView.as_view(), name='export'),
] 