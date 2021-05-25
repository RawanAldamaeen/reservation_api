from datetime import datetime

from annoying.functions import get_object_or_None
from rest_framework import serializers
from ..models.reservation import Reservation
from shifts.models.shifts import Shift
from django.utils.translation import gettext as _


class NewReservationView(serializers.ModelSerializer):  # create new reservation serializer
    date = serializers.DateField(required=True, format="%Y-%m-%d")
    time = serializers.TimeField(required=True, format='%I:%M %p')

    class Meta:
        model = Reservation
        fields = ['doctor_id', 'date', 'time']

    def validate(self, attrs):
        doctor_id = attrs.get('doctor_id', '')
        date = attrs.get('date', '')
        time = attrs.get('time', '')

        # Check doctor available day
        day = datetime.strftime(date,"%A")
        doctor_shifts = get_object_or_None(Shift, day=day, doctor_id=doctor_id)
        if doctor_shifts is None:
            raise serializers.ValidationError(
                {'error': _('Doctor is unavailable on this day, please choose another day')}
            )

        # Check doctor available time
        # 1- check if the reservation time in the doctor shift range
        start = datetime.strptime(doctor_shifts.start_time, '%I:%M %p')
        end = datetime.strptime(doctor_shifts.end_time, '%I:%M %p')

        if time < start.time() or time > end.time():
            raise serializers.ValidationError(
                {'error': _(f'Doctor is unavailable on this time, please choose time between {start.time()} and {end.time()}')}
            )

        # 2- Check if the time of the reservations isn't conflict with other reservations
        reservations = Reservation.objects.filter(doctor_id=doctor_id)
        for x in reservations:
            if x.time == time and x.date == date and not x.status == 'confirm':
                raise serializers.ValidationError(
                    {'error': _(f'Doctor is unavailable on this time, please choose another hour between {start.time()} and {end.time()}')}
                )

        return super().validate(attrs)

    def create(self, validated_data):
        data = validated_data
        data['status'] = 'new'

        return Reservation.objects.create(**validated_data)
