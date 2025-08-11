from django.contrib import admin
from .models import Kapal, JenisIkan, WPP, TangkapanIkan

from django.contrib import admin
from .models import Kapal

@admin.register(Kapal)
class KapalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_kapal', 'pemilik', 'nahkoda')
    list_filter = ('pemilik', 'nahkoda')
    search_fields = ('nama_kapal', 'pemilik__noreg_bkp', 'nahkoda__noreg_bkp')


@admin.register(JenisIkan)
class JenisIkanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(WPP)
class WPPAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name',)

@admin.register(TangkapanIkan)
class TangkapanIkanAdmin(admin.ModelAdmin):
    list_display = ('id', 'kapal', 'jenis_ikan', 'weight', 'location')
    list_filter = ('kapal', 'jenis_ikan', 'location')
    search_fields = ('kapal__kapal_name', 'jenis_ikan__name', 'location__name')
