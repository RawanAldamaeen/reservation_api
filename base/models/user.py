from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class User(AbstractUser):   # Users types model
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    language = models.CharField(choices=[('ar', _('Arabic')), ('en', _('English'))], default='en', max_length=32)
