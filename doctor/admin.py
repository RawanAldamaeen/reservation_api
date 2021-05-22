from django.contrib import admin
from .models.doctor import Doctor
from .models.specialty import Specialty

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Specialty)
