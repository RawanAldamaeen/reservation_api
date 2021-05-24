from django.contrib import admin
from .models.shifts import Shift

# Register your models here.

class ShiftsAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'id')


admin.site.register(Shift, ShiftsAdmin)
