#!/usr/bin/env python3
"""
Test script untuk memverifikasi upload dataset dengan autentikasi
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

def test_upload_with_auth():
    """Test upload dataset dengan autentikasi"""
    print("=== Testing Dataset Upload with Authentication ===")
    
    # 1. Test login
    print("\n=== Testing Login ===")
    session = requests.Session()
    
    # Get CSRF token first
    login_url = "http://localhost:8002/"
    response = session.get(login_url)
    
    if response.status_code == 200:
        print("✅ Login page accessible")
        
        # Try to login
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'csrfmiddlewaretoken': session.cookies.get('csrftoken', '')
        }
        
        response = session.post(login_url, data=login_data)
        
        if response.status_code == 200 and 'dashboard' in response.url:
            print("✅ Login successful!")
        else:
            print("❌ Login failed")
            print(f"Response status: {response.status_code}")
            print(f"Response URL: {response.url}")
            return
    else:
        print(f"❌ Cannot access login page: {response.status_code}")
        return
    
    # 2. Test datasets page
    print("\n=== Testing Datasets Page ===")
    datasets_url = "http://localhost:8002/datasets/"
    response = session.get(datasets_url)
    
    if response.status_code == 200:
        print("✅ Datasets page accessible")
        if 'Your Datasets' in response.text:
            print("✅ Datasets page content correct")
        else:
            print("❌ Datasets page content incorrect")
    else:
        print(f"❌ Cannot access datasets page: {response.status_code}")
    
    # 3. Test dataset upload
    print("\n=== Testing Dataset Upload ===")
    upload_url = "http://localhost:8002/datasets/"
    
    # Create a test CSV file
    test_csv_content = """Tahun,Bulan,stok_ikan
2021,1,100.5
2021,2,120.3
2021,3,95.7
2021,4,110.2
2021,5,105.8"""
    
    with open('test_dataset.csv', 'w') as f:
        f.write(test_csv_content)
    
    # Upload the file
    with open('test_dataset.csv', 'rb') as f:
        files = {
            'file': ('test_dataset.csv', f, 'text/csv')
        }
        data = {
            'name': 'Test Dataset',
            'description': 'Test dataset for upload verification',
            'csrfmiddlewaretoken': session.cookies.get('csrftoken', '')
        }
        
        response = session.post(upload_url, data=data, files=files)
        
        if response.status_code == 302:  # Redirect after successful upload
            print("✅ Dataset upload successful!")
        else:
            print(f"❌ Dataset upload failed: {response.status_code}")
            print(f"Response content: {response.text[:200]}...")
    
    # 4. Check if dataset was created
    print("\n=== Checking Database ===")
    datasets = Dataset.objects.all()
    print(f"Total datasets in database: {datasets.count()}")
    
    for dataset in datasets:
        print(f"  - {dataset.name} (User: {dataset.user.username if dataset.user else 'None'})")
    
    # Clean up
    if os.path.exists('test_dataset.csv'):
        os.remove('test_dataset.csv')

if __name__ == "__main__":
    test_upload_with_auth() 