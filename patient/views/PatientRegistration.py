from django.urls import reverse
from django.utils import translation
from rest_framework import generics
from ..serializers.NewPatientSerializer import CreatePatientSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..models.patient import Patient
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _
from base.models.user import User


class PatientCreate(generics.CreateAPIView):  # create new patient view
    queryset = Patient.objects.all()
    serializer_class = CreatePatientSerializer

    def post(self, request, *args, **kwargs):  # perform post request
        data = request.data
        serializer = CreatePatientSerializer(data=request.data)

        # invalid data response
        if not serializer.is_valid():
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data={"status": status.HTTP_422_UNPROCESSABLE_ENTITY, "data": {},
                                  'error': serializer.errors, 'meta': {}})
        serializer.save()

        # Activate account email
        email = data['email']
        user = User.objects.get(email=email)

        # Get the user language
        patient = Patient.objects.get(user=user)
        lang = patient.language
        translation.activate(lang)

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse("user-verify")
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        email_body = _('Hi, Use the link below to verify your email \n') + absurl
        email_subject = _('Activate the account')
        subject = email_subject
        message = email_body
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)

        return Response(status=status.HTTP_201_CREATED,
                        data={"status": status.HTTP_201_CREATED, "data": serializer.data, 'meta': {}})



