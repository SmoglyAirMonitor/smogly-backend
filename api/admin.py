from django.contrib import admin
from django import forms
from .models import Station, Metering


class StationAdminForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = '__all__'


class StationAdmin(admin.ModelAdmin):
    form = StationAdminForm
    list_display = ['name', 'created', 'updated', 'type', 'notes', 'position', 'country', 'state',
                    'county', 'community', 'city', 'district']
    readonly_fields = ['created', 'updated']
    
admin.site.register(Station, StationAdmin)


class MeteringAdminForm(forms.ModelForm):
    class Meta:
        model = Metering
        fields = '__all__'


class MeteringAdmin(admin.ModelAdmin):
    form = MeteringAdminForm
    list_display = ['created', 'pm25', 'pm10', 'temperature', 'humidity']
    readonly_fields = ['created']

admin.site.register(Metering, MeteringAdmin)
