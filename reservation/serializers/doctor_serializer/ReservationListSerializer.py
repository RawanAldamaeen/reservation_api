from rest_framework import serializers
from reservation.models.reservation import Reservation
from patient.models.patient import Patient


class PatientName(serializers.ModelSerializer):  # class to return patient name
    class Meta:
        model = Patient
        fields = ['name']


class ReservationListSerializer(serializers.ModelSerializer):  # list of reservations serializer

    patient_id = PatientName(many=False, read_only=False)
    actions = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'patient_id', 'time', 'date', 'status', 'actions']

    def get_actions(self, obj):
        if obj.status == 'new':
            status_choices = ('confirm', 'canceled')
        elif obj.status == 'confirm':
            status_choices = ('canceled', 'closed')
        else:
            status_choices = 'closed'

        return status_choices
