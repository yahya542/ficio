from django.contrib import admin
from .models import Ship, Tangkapan  # Ganti FishCatch -> Tangkapan

admin.site.register(Ship)
admin.site.register(Tangkapan)
