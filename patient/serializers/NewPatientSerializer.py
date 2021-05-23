from django.contrib.auth.password_validation import validate_password
from django.core import validators
from rest_framework import serializers
from ..models.patient import Patient
from base.models.user import User
from django.utils.translation import gettext as _


class CreatePatientSerializer(serializers.ModelSerializer):  # Create new patient request serializer
    language_choice = [
        ('ar', 'Arabic'),
        ('en', 'English'),
    ]
    gender_choice = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    username = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(validators=[validate_password],
                                     style={'input_type': 'password', 'placeholder': 'Password'},
                                     max_length=30, write_only=True)
    email = serializers.EmailField(max_length=250, validators=[validators.validate_email], write_only=True)
    name = serializers.CharField(validators=[validators.MinLengthValidator(2)])
    phone = serializers.CharField()
    photo = serializers.ImageField(required=False, write_only=True, default=None)
    language = serializers.ChoiceField(required=False, choices=language_choice, default='en')
    gender = serializers.ChoiceField(required=False, choices=gender_choice, default='none')

    class Meta:
        model = Patient
        fields = ['username', 'password', 'email', 'name', 'phone', 'photo', 'language', 'gender']
        optional_fields = ['photo', 'language', 'gender']

    def validate(self, attrs):  # validate patient data
        password = attrs.get('password', '')
        email = attrs.get('email', '')
        phone = attrs.get('phone', '')
        username = attrs.get('username', '')
        name = attrs.get('name', '')

        # Username validations
        if len(username) < 5 or len(username) > 100:
            raise serializers.ValidationError(
                {_('username'): _('username length should be between 5 - 100 characters')}
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {_('username'): _('username is already in use')}
            )

        # Password validation
        if len(password) < 8 or len(password) > 30:
            raise serializers.ValidationError(
                {_('password'): _('Password length should be between 8 - 30 characters')}
            )

        # Email validation
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {_('email'): _('Email is already in use')}
            )

        # Phone validations
        if len(phone) < 10 or len(phone) > 15:
            raise serializers.ValidationError(
                {_('phone'): _('Phone length should be between 10 - 15 characters')}
            )
        if Patient.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                {_('phone'): _('phone is already in use')}
            )

        # Name validation
        if len(name) < 5 or len(name) > 100:
            raise serializers.ValidationError(
                {_('name'): _('name length should be between 5 - 100 characters')}
            )

        return super().validate(attrs)

    def create(self, validated_data):  # create new doctor function
        data = validated_data
        user = User()
        user.username = data['username']
        user.email = data['email']
        user.set_password(data['password'])
        user.is_active = False
        user.is_patient = True
        user.save()
        patient = Patient()
        patient.user = user
        patient.name = data['name']
        patient.phone = data['phone']
        patient.language = data['language']
        patient.gender = data['gender']
        patient.photo = data['photo']
        patient.save()
        return patient
