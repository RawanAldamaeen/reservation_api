from django.contrib import admin
from .models.user import User
# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'id')


admin.site.register(User, UsersAdmin)