#!/usr/bin/env python3
"""
Script untuk mengupload dataset CSV ke database
"""
import os
import sys
import django
from django.core.files import File

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fishcast.settings')
django.setup()

from api.models import Dataset

def upload_dataset():
    """Upload dataset CSV ke database"""
    print("=== Uploading Dataset ===")
    
    # Check if dataset already exists
    existing_datasets = Dataset.objects.filter(name__icontains='simulasi')
    if existing_datasets.exists():
        print("Dataset already exists:")
        for dataset in existing_datasets:
            print(f"  - {dataset.name} (ID: {dataset.id})")
        return existing_datasets.first()
    
    # Upload new dataset
    csv_path = "media/datasets/simulasi_perikanan.csv"
    
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found!")
        return None
    
    try:
        with open(csv_path, 'rb') as f:
            dataset = Dataset.objects.create(
                name="Data Simulasi Perikanan",
                description="Dataset simulasi data perikanan dengan berbagai variabel",
                file=File(f, name="simulasi_perikanan.csv")
            )
        
        print(f"✅ Dataset uploaded successfully!")
        print(f"  Name: {dataset.name}")
        print(f"  ID: {dataset.id}")
        print(f"  File: {dataset.file.name}")
        
        return dataset
        
    except Exception as e:
        print(f"❌ Error uploading dataset: {e}")
        return None

if __name__ == "__main__":
    upload_dataset() 