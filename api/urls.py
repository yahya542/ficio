from django.urls import path
from . import api_views as views


urlpatterns = [
    # Auth
   
    # Health Check
    path('health/', views.health_check, name='health_check'),
    

    
]