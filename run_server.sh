#!/bin/bash
# Script to run the Django development server

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Installing PostgreSQL adapter..."
pip install psycopg2-binary

echo "Running migrations..."
python manage.py migrate

echo "Starting Django development server..."
python manage.py runserver