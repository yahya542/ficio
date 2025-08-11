from django.urls import path
from . import views


urlpatterns = [
    # Kapal
    path('kapal/input/', views.input_kapal, name='input_kapal'),
    path('list-kapal/', views.list_kapal, name='list_kapal'),

    # Tangkapan
    path('tangkapan/input/', views.input_tangkapan_batch, name='input_tangkapan_batch'),
    path('tangkapan/list/', views.list_tangkapan, name='list_tangkapan'),

    # Master Data
    path('master/jenis-ikan/', views.list_jenis_ikan, name='list_jenis_ikan'),
    path('master/wpp/', views.list_wpp, name='list_wpp'),
]
