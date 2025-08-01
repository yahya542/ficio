# 🐟 FishCast AI - Aplikasi Analisis Data Perikanan

FishCast AI adalah aplikasi web yang menggabungkan dashboard interaktif dengan API untuk analisis data perikanan menggunakan machine learning. Aplikasi ini dirancang untuk membantu peneliti dan praktisi perikanan dalam melakukan prediksi, optimisasi, dan analisis korelasi data perikanan.

## ✨ Fitur Utama

- **📊 Dashboard Interaktif**: Interface web yang user-friendly dengan statistik real-time
- **📁 Upload Dataset**: Kemampuan untuk mengunggah file CSV dengan validasi
- **🤖 Prediksi Multi-Model**: Linear Regression, LSTM, GRU, BiLSTM, RNN
- **⚡ Optimisasi NSGA-III**: Multi-objective optimization dengan visualisasi Pareto front
- **📈 Analisis Korelasi**: Visualisasi matriks korelasi dengan heatmap
- **🔌 API RESTful**: Endpoint untuk integrasi dengan aplikasi lain
- **📱 Responsive Design**: Berfungsi optimal di desktop, tablet, dan mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- virtual environment (recommended)

### Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd backend
```

2. **Setup Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser (Optional)**
```bash
python manage.py createsuperuser
```

6. **Run Development Server**
```bash
python manage.py runserver 8001
```

7. **Access Application**
- **Dashboard**: http://localhost:8001/
- **Admin Panel**: http://localhost:8001/admin/
- **API Base**: http://localhost:8001/api/

## 📁 Struktur Proyek

```
backend/
├── api/                    # Django app utama
│   ├── models.py          # Model database
│   ├── views.py           # Views (API + Dashboard)
│   ├── urls.py            # URL routing API
│   ├── serializers.py     # DRF serializers
│   └── ml_models.py       # Machine learning logic
├── fishcast/              # Django project settings
│   ├── settings.py        # Konfigurasi aplikasi
│   └── urls.py            # URL routing utama
├── templates/             # HTML templates
│   ├── base.html          # Template dasar
│   ├── dashboard.html     # Halaman dashboard
│   ├── datasets.html      # Manajemen dataset
│   ├── predictions.html   # Hasil prediksi
│   ├── optimization.html  # Hasil optimisasi
│   └── correlation.html   # Analisis korelasi
├── media/                 # File uploads
├── staticfiles/           # Static files
└── manage.py             # Django management
```

## 🎯 Cara Penggunaan

### 1. Upload Dataset
1. Buka halaman **Datasets**
2. Klik **"Upload Dataset"**
3. Isi nama dataset
4. Pilih file CSV
5. Tambah deskripsi (opsional)
6. Klik **"Upload"**

### 2. Run Prediction
1. Buka halaman **Predictions**
2. Klik **"Run New Prediction"**
3. Pilih dataset
4. Pilih model(s) yang diinginkan
5. Klik **"Run Prediction"**
6. Tunggu proses selesai
7. Lihat hasil di tabel

### 3. Run Optimization
1. Buka halaman **Optimization**
2. Klik **"Run New Optimization"**
3. Pilih dataset
4. Set parameter (population_size, generations)
5. Klik **"Run Optimization"**
6. Lihat Pareto front chart

### 4. Run Correlation Analysis
1. Buka halaman **Correlation Analysis**
2. Klik **"Run New Analysis"**
3. Pilih dataset
4. Klik **"Run Analysis"**
5. Lihat correlation matrix heatmap

## 📊 Format Dataset

Dataset harus dalam format CSV dengan struktur:
```csv
date,temperature,salinity,ph,dissolved_oxygen,fish_count
2024-01-01,25.5,35.2,7.8,6.2,150
2024-01-02,26.1,34.8,7.9,6.5,165
...
```

**Requirements:**
- Header row dengan nama kolom
- Data numerik untuk analisis
- Minimal 10 baris data
- Maksimal 10MB file size

## 🔌 API Endpoints

### Base URL: `http://localhost:8001/api/`

### Health Check
```
GET /api/health/
Response: {"status": "healthy"}
```

### Dataset Endpoints
```
GET    /api/datasets/           # List datasets
POST   /api/datasets/           # Upload dataset
GET    /api/datasets/{id}/      # Get dataset detail
DELETE /api/datasets/{id}/      # Delete dataset
```

### Prediction Endpoints
```
POST   /api/predict/            # Run prediction
GET    /api/predictions/        # List predictions
GET    /api/predictions/{id}/   # Get prediction detail
```

### Optimization Endpoints
```
POST   /api/optimize/           # Run optimization
GET    /api/optimization-results/        # List results
GET    /api/optimization-results/{id}/   # Get result detail
```

### Correlation Endpoints
```
POST   /api/correlation/        # Run correlation analysis
GET    /api/correlation-results/         # List results
GET    /api/correlation-results/{id}/    # Get result detail
```

### Export Endpoint
```
GET    /api/export/{prediction_id}/      # Export prediction results
```

## 🛠️ Development

### Tech Stack
- **Backend**: Django 5.2.4 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome 6
- **ML Libraries**: Pandas, NumPy

### Environment Variables
```bash
# settings.py
DEBUG = True
SECRET_KEY = 'your-secret-key'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### Database Models
- **Dataset**: Menyimpan informasi dataset yang diupload
- **Prediction**: Hasil prediksi dari berbagai model ML
- **OptimizationResult**: Hasil optimisasi multi-objective
- **CorrelationAnalysis**: Hasil analisis korelasi

## 📚 Dokumentasi

Dokumentasi lengkap tersedia dalam format Markdown dan dapat dikonversi ke Word/PDF:

### File Dokumentasi
- `DOCUMENTATION_PART1.md` - Pendahuluan, Arsitektur, Database, Alur
- `DOCUMENTATION_PART2.md` - Frontend, API, ML Pipeline, Penggunaan
- `DOCUMENTATION_PART3.md` - Troubleshooting, Pengembangan, Kesimpulan
- `README_DOCUMENTATION.md` - Cara konversi dokumentasi

### Konversi Dokumentasi
```bash
# Install pandoc
sudo apt-get install pandoc

# Convert to Word
python convert_documentation.py --format word

# Convert to PDF
python convert_documentation.py --format pdf

# Convert to all formats
python convert_documentation.py --format all
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill process on port 8001
sudo lsof -ti:8001 | xargs kill -9

# Atau gunakan port lain
python manage.py runserver 8002
```

#### ModuleNotFoundError: No module named 'pandas'
```bash
pip install pandas numpy
```

#### Database Migration Error
```bash
python manage.py migrate api zero
rm api/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

#### File Upload Error
- Cek permission folder `media/`
- Pastikan file tidak terlalu besar
- Validasi format CSV

### Debug Mode
```python
# settings.py
DEBUG = True
```

## 🚀 Deployment

### Production Setup
1. **Install Dependencies**
```bash
pip install gunicorn psycopg2-binary
```

2. **Configure Database**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fishcast_db',
        'USER': 'fishcast_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Collect Static Files**
```bash
python manage.py collectstatic
```

4. **Run with Gunicorn**
```bash
gunicorn fishcast.wsgi:application --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "fishcast.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

Untuk pertanyaan atau dukungan teknis:
- **Email**: support@fishcast.ai
- **Documentation**: https://docs.fishcast.ai
- **GitHub**: https://github.com/fishcast-ai
- **Issues**: https://github.com/fishcast-ai/issues

## 🙏 Acknowledgments

- Django team untuk framework yang powerful
- Bootstrap team untuk UI components
- Chart.js team untuk visualisasi data
- Pandas dan NumPy teams untuk data processing

---

*FishCast AI - Empowering Fisheries with AI*
*Version: 1.0.0*
*Django Version: 5.2.4*
*Status: Development Complete - Ready for Production* 