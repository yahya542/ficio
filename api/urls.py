from django.urls import path
from . import views

urlpatterns = [
    path('ship/', views.input_ship, name='input_ship'),
    path('ships/', views.list_ships, name='list_ships'),
    path('tangkapan/', views.input_tangkapan, name='input_tangkapan'),
    path('tangkapans/', views.list_tangkapan, name='list_tangkapan'),
]
