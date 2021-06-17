from django.conf import settings
from django.core.mail import send_mail
from rest_framework import authentication, status
from rest_framework.views import APIView
from reservation.serializers.doctor_serializer.ConfirmReservationSerializer import ConfirmReservationSerializer
from reservation.models.reservation import Reservation
from reservations.response import Responses
from django.utils.translation import gettext as _
from base.models.user import User
from django.utils import translation


def send_confirm_message(email):        # send confirm email function
    user = User.objects.get(email=email)
    patient_language = user.language
    translation.activate(patient_language)

    email_title = _('Reservation Confirmed')
    email_message = _(
        'Hello, your reservation confirmed, be sure to be on the hospital on time')
    subject = email_title
    message = email_message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)


class ConfirmReservationView(APIView):  # confirm patient reservation view
    queryset = Reservation.objects.all()
    serializer_class = ConfirmReservationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):  # Perform PUT request
        pk = self.kwargs.get('pk')
        reservation = Reservation.objects.get(pk=pk)

        # check if user is not doctor
        if request.user.is_anonymous or not request.user.is_doctor or not reservation.doctor_id == request.user.doctor:
            return Responses.getErrorResponse(status=status.HTTP_403_FORBIDDEN,
                                              error=_('your not allowed to perform this action'))

        reservation.status = 'confirm'
        reservation.save()
        serializer = ConfirmReservationSerializer(reservation)
        email = reservation.patient_id.user.email
        send_confirm_message(email)
        return Responses.getResponse(status=status.HTTP_200_OK, data=serializer.data)
