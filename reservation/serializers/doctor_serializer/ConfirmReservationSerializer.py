from rest_framework import serializers
from reservation.models.reservation import Reservation
from patient.models.patient import Patient


class PatientName(serializers.ModelSerializer):  # class to return patient name
    class Meta:
        model = Patient
        fields = ['name']


class ConfirmReservationSerializer(serializers.ModelSerializer):  # reservation data serializer
    patient_id = PatientName(many=False, read_only=False)

    class Meta:
        model = Reservation
        fields = ['id','patient_id', 'time', 'date', 'status']
