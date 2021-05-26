from datetime import datetime

from rest_framework import serializers
from ..models.shifts import Shift
from django.utils.translation import gettext as _


class CreateShiftSerializer(serializers.ModelSerializer):
    day_choices = [('Sunday', 'Sunday'),
                   ('Monday', 'Monday'),
                   ('Tuesday', 'Tuesday'),
                   ('Wednesday', 'Wednesday'),
                   ('Thursday', 'Thursday'),
                   ('Friday', 'Friday'),
                   ('Saturday', 'Saturday')]

    start_time = serializers.CharField(required=False)
    end_time = serializers.CharField(required=False)
    day = serializers.ChoiceField(choices=day_choices, required=True)
    all_day = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Shift
        fields = ["day", "all_day", "start_time", "end_time"]
        optional_fields = ["all_day", "start_time", "end_time"]

    def validate(self, attrs):  # validate shift data
        start_time = attrs.get('start_time', '')
        end_time = attrs.get('end_time', '')
        all_day = attrs.get('all_day', '')

        if not all_day and not start_time and not end_time:
            raise serializers.ValidationError(
                {'error': 'start time and end time is required'}
            )

        if start_time and end_time:
            start = datetime.strptime(start_time, '%I:%M %p')
            end = datetime.strptime(end_time, '%I:%M %p')

            if start > end:
                raise serializers.ValidationError(
                    {_('start time'): _('shift start time should be before shift end time')}
                )
        return super().validate(attrs)

    def create(self, validated_data):
        data = validated_data
        all_day = data['all_day']

        if all_day:
            data['start_time'] = None
            data['end_time'] = None

        return Shift.objects.create(**validated_data)


