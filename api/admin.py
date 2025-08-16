from django.contrib import admin
from .models import Kapal, JenisIkan, WPP, TangkapanIkan, Profile

@admin.register(Kapal)
class KapalAdmin(admin.ModelAdmin):
    list_display = ('id', 'no_reg_bkp', 'nama_kapal', 'get_pemilik', 'get_nahkoda')
    search_fields = ('no_reg_bkp', 'nama_kapal')

    def get_pemilik(self, obj):
        profile = obj.profiles.filter(role='pemilik_kapal').select_related('user').first()
        return profile.user.username if profile else "-"
    get_pemilik.short_description = "Pemilik Kapal"

    def get_nahkoda(self, obj):
        profile = obj.profiles.filter(role='nahkoda').select_related('user').first()
        return profile.user.username if profile else "-"
    get_nahkoda.short_description = "Nahkoda"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'kapal', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'kapal__no_reg_bkp')


@admin.register(JenisIkan)
class JenisIkanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')
    search_fields = ('nama',)


@admin.register(WPP)
class WPPAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name',)


@admin.register(TangkapanIkan)
class TangkapanIkanAdmin(admin.ModelAdmin):
    list_display = ('id', 'kapal', 'jenis_ikan', 'weight', 'location')
    list_filter = ('kapal', 'jenis_ikan', 'location')
    search_fields = ('kapal__nama_kapal', 'jenis_ikan__name', 'location__name')
