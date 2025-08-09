from django.urls import path
from . import views
from .views import IkanViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IkanViewSet, valid_id_view


router = DefaultRouter()
router.register(r'ikan', IkanViewSet, basename='ikan')



urlpatterns = [
    path('ship/', views.input_ship, name='input_ship'),
    path('ships/', views.list_ships, name='list_ships'),
    path('tangkapan/', views.input_tangkapan, name='input_tangkapan'),
    path('tangkapans/', views.list_tangkapan, name='list_tangkapan'),
    path('', include(router.urls)),
    path('valid_id/', valid_id_view),


   


]
