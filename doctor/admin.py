from django.contrib import admin
from .models.doctor import Doctor
from .models.specialty import Specialty


# Register your models here.

class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')


admin.site.register(Doctor, DoctorsAdmin)
admin.site.register(Specialty)
