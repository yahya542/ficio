#!/usr/bin/env python3
"""
Test script untuk memverifikasi fungsi prediksi
"""
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fishcast.settings')
django.setup()

from api.models import Dataset, Prediction
from api.ml_models import ml_engine

def test_prediction():
    """Test fungsi prediksi"""
    print("=== Testing Prediction Functionality ===")
    
    # 1. Check if dataset exists
    datasets = Dataset.objects.all()
    print(f"Found {datasets.count()} datasets")
    
    if datasets.count() == 0:
        print("No datasets found. Please upload a CSV file first.")
        return
    
    # Get first dataset
    dataset = datasets.first()
    print(f"Using dataset: {dataset.name}")
    print(f"File path: {dataset.file.path}")
    
    # 2. Test ML engine directly
    print("\n=== Testing ML Engine ===")
    try:
        results = ml_engine.train_and_predict(
            dataset.id, 
            dataset.file.path, 
            ['Linear']
        )
        print("ML Engine Results:")
        for model_name, result in results.items():
            print(f"  {model_name}:")
            print(f"    MSE: {result['mse']:.4f}")
            print(f"    MAE: {result['mae']:.4f}")
            print(f"    Predictions: {len(result['predictions'])} values")
            print(f"    Actual: {len(result['actual_values'])} values")
    except Exception as e:
        print(f"Error in ML engine: {e}")
        return
    
    # 3. Test API endpoint
    print("\n=== Testing API Endpoint ===")
    try:
        url = "http://localhost:8000/api/predict/"
        data = {
            "dataset_id": dataset.id,
            "models": ["Linear"]
        }
        
        response = requests.post(url, json=data)
        print(f"API Response Status: {response.status_code}")
        print(f"API Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ API prediction successful!")
        else:
            print("❌ API prediction failed!")
            
    except Exception as e:
        print(f"Error testing API: {e}")
    
    # 4. Check predictions in database
    print("\n=== Checking Database ===")
    predictions = Prediction.objects.all()
    print(f"Total predictions in database: {predictions.count()}")
    
    for pred in predictions:
        print(f"  - {pred.model_type} on {pred.dataset.name}")
        print(f"    MSE: {pred.mse:.4f}, MAE: {pred.mae:.4f}")
        print(f"    Created: {pred.created_at}")

if __name__ == "__main__":
    test_prediction() 