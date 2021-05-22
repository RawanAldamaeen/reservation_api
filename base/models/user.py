from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):   # Users types model
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)