from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.utils import translation
from base.models.user import User
from .specialty import Specialty


class Doctor(models.Model):     # Doctor model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=15)
    photo = models.ImageField(upload_to='doctors/dr_pics', blank=True, default=None)
    degree_copy = models.ImageField(upload_to='doctors/dr_degree_copy', default=None)
    gender = models.CharField(choices=[('Male', _('Male')), ('Female', _('Female'))], default=None, max_length=32)
    specialty_id = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    language = models.CharField(choices=[('ar', _('Arabic')), ('en', _('English'))], default='en', max_length=32)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(signals.post_save, sender=Doctor)
def new_doctor_account_emails(sender, instance, **kwargs):  # Send welcome email signals
    if instance:
        # Doctor welcome email
        lang = instance.language
        translation.activate(lang)
        email_title = _('Thank you for registering with us')
        email_message = _('Hello, thank you for registering in the reservations system. your account will be activated soon by the admin.')
        subject = email_title
        message = email_message
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email, ]
        send_mail(subject, message, email_from, recipient_list)
