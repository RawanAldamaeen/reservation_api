from django.contrib import admin
from .models.patient import Patient


# Register your models here.

class PatientsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(Patient, PatientsAdmin)
