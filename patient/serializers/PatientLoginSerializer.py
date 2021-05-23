from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from base.models.user import User
from django.utils.translation import gettext as _


class PatientLoginSerializers(serializers.ModelSerializer):  # Patient login serializer
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(validators=[validate_password],
                                     style={'input_type': 'password', 'placeholder': 'Password'},
                                     max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username and not password:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        if not user.is_active:
            msg = _('your account is still inactive, check your email box for activation email')
            raise serializers.ValidationError(msg, code='authorization')

        if not user.is_patient:
            msg = _('this page for patient login only')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
