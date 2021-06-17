from django.db import models
from doctor.models.doctor import Doctor
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

time_regex = RegexValidator(regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s?(?:AM|PM|am|pm)')


class Shift(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    all_day = models.BooleanField(default=False)
    start_time = models.CharField(validators=[time_regex], max_length=20, default=None, blank=True, null=True)
    end_time = models.CharField(validators=[time_regex], max_length=20, default=None, blank=True, null=True)
    day = models.CharField(choices=[('Sunday', _('Sunday')),
                                    ('Monday', _('Monday')),
                                    ('Tuesday', _('Tuesday')),
                                    ('Wednesday', _('Wednesday')),
                                    ('Thursday', _('Thursday')),
                                    ('Friday', _('Friday')),
                                    ('Saturday', _('Saturday'))], default=None, max_length=10)
