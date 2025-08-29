from django.urls import path
from .views import views
from .views import admin_views as admin
from .views import kuota_views as kuota
from .permissions import manage_access, list_access

urlpatterns = [
    # Kapal
    path('kapal/input/', views.input_kapal, name='input_kapal'),
    path('list-kapal/', views.list_kapal, name='list_kapal'),

    # Tangkapan
    path('tangkapan/input/', views.input_tangkapan_batch, name='input_tangkapan_batch'),
   

    # Master Data
    path('master/jenis-ikan/', views.list_jenis_ikan, name='list_jenis_ikan'),
    path('master/wpp/', views.list_wpp, name='list_wpp'),

    #dhistory tangkapan
    path('kapal/history/', views.kapal_history, name='kapal_history_user'),

    # History kapal perkapal untuk admin (wajib sertakan no_reg_bkp)
    path('kapal/<str:no_buku_kapal>/history/', views.kapal_history, name='kapal_history_admin'),

    # Admin Views
    path("import/kapal/", admin.import_kapal_csv, name="import_kapal"),
    path("import/jenis-ikan/", admin.import_jenis_ikan_csv, name="import_jenis_ikan"),
    path("import/wpp/", admin.import_wpp_csv, name="import_wpp"),

    #regulator 
    path("input/kuota/", kuota.AturKuotaKapalView.as_view(), name="import_kuota"),

    #superuser 
    path("atur/akses/", manage_access, name="atur_akses"), 
    path("lihat/akses/", list_access, name="lihat_akses"),


]
