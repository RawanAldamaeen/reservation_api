from django.utils.translation import gettext as _
from base.models.user import User
from django.db import models


class Patient(models.Model):     # Patient model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=15)
    photo = models.ImageField(upload_to='patients/patients_pics', blank=True, default=None)
    gender = models.CharField(choices=[('Male', _('Male')), ('Female', _('Female'))], default=None, max_length=32)
    language = models.CharField(choices=[('ar', _('Arabic')), ('en', _('English'))], default='en', max_length=32)

    def __str__(self):
        return f'{self.user.username} Profile'
