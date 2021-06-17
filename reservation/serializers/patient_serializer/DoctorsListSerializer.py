from rest_framework import serializers
from doctor.models.doctor import Doctor
from doctor.models.specialty import Specialty


class DoctorSpecialty(serializers.ModelSerializer):  # class to return specialty in English
    class Meta:
        model = Specialty
        fields = ['specialty_en']


class DoctorsListSerializer(serializers.ModelSerializer):  # list of doctors and their specialty in English serializer
    specialty_id = DoctorSpecialty(many=False, read_only=False)

    class Meta:
        model = Doctor
        fields = ['name', 'specialty_id']


class DoctorSpecialtyAR(serializers.ModelSerializer):  # class to return specialty in Arabic
    class Meta:
        model = Specialty
        fields = ['specialty_ar']


class DoctorsListARSerializer(serializers.ModelSerializer):  # list of doctors and their specialty in English serializer
    specialty_id = DoctorSpecialtyAR(many=False, read_only=False)

    class Meta:
        model = Doctor
        fields = ['name', 'specialty_id']
