from django.db import models
from doctor.models.doctor import Doctor
from patient.models import Patient
from django.utils.translation import gettext as _


class Reservation(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rejection_reason = models.CharField(default=None, null=True, max_length=250)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        choices=[('new', _('new')),
                 ('confirm', _('confirm')),
                 ('canceled', _('canceled')),
                 ('closed', _('closed'))],
        default='new', max_length=20)
