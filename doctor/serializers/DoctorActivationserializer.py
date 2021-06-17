
from rest_framework import serializers
from base.models.user import User


class ActivateDoctorSerializer(serializers.ModelSerializer):  # activate doctor request serializer
    username = serializers.CharField()
    is_active = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'is_active']