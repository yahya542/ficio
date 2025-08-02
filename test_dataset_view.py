#!/usr/bin/env python3
"""
Test script untuk memverifikasi fungsi dataset view
"""
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fishcast.settings')
django.setup()

from api.models import Dataset, User, Ship

def test_dataset_view():
    """Test fungsi dataset view"""
    print("=== Testing Dataset View Functionality ===")
    
    # 1. Check if datasets exist
    datasets = Dataset.objects.all()
    print(f"Found {datasets.count()} datasets")
    
    if datasets.count() == 0:
        print("No datasets found.")
        return
    
    # Get first dataset
    dataset = datasets.first()
    print(f"Using dataset: {dataset.name}")
    print(f"File path: {dataset.file.path}")
    
    # 2. Test dataset preview API
    print("\n=== Testing Dataset Preview API ===")
    try:
        url = f"http://localhost:8001/api/datasets/{dataset.id}/preview/"
        response = requests.get(url)
        print(f"Preview API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dataset preview successful!")
            print(f"   Total rows: {data.get('total_rows', 'N/A')}")
            print(f"   Columns: {data.get('columns', [])}")
            print(f"   Preview rows: {len(data.get('data', []))}")
            
            # Show first few rows
            if data.get('data'):
                print("\n   First row data:")
                first_row = data['data'][0]
                for key, value in first_row.items():
                    print(f"     {key}: {value}")
        else:
            print(f"❌ Dataset preview failed: {response.text}")
            
    except Exception as e:
        print(f"Error testing preview API: {e}")
    
    # 3. Test dataset download API
    print("\n=== Testing Dataset Download API ===")
    try:
        url = f"http://localhost:8001/api/datasets/{dataset.id}/download/"
        response = requests.get(url)
        print(f"Download API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Dataset download successful!")
            print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"   Content-Disposition: {response.headers.get('Content-Disposition', 'N/A')}")
            print(f"   Content length: {len(response.content)} bytes")
        else:
            print(f"❌ Dataset download failed: {response.text}")
            
    except Exception as e:
        print(f"Error testing download API: {e}")
    
    # 4. Test dataset detail API
    print("\n=== Testing Dataset Detail API ===")
    try:
        url = f"http://localhost:8001/api/datasets/{dataset.id}/"
        response = requests.get(url)
        print(f"Detail API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dataset detail successful!")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   File: {data.get('file', 'N/A')}")
            print(f"   Uploaded: {data.get('uploaded_at', 'N/A')}")
            print(f"   Description: {data.get('description', 'N/A')}")
        else:
            print(f"❌ Dataset detail failed: {response.text}")
            
    except Exception as e:
        print(f"Error testing detail API: {e}")

if __name__ == "__main__":
    test_dataset_view() 