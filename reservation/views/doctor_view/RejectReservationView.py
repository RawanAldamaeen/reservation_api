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


def send_reject_message(email, reason):        # send reject email function
    user = User.objects.get(email=email)
    patient_language = user.language
    translation.activate(patient_language)

    email_title = _('Reservation rejected')
    email_message = _(
        f'Hello, your reservation is rejected, for the reason: {reason}, please choose another time')
    subject = email_title
    message = email_message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)


class RejectReservationView(APIView):  # reject patient reservation view
    queryset = Reservation.objects.all()
    serializer_class = ConfirmReservationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):  # Perform PUT request
        data = request.data
        pk = self.kwargs.get('pk')
        reservation = Reservation.objects.get(pk=pk)

        # check if user is not doctor
        if request.user.is_anonymous or not request.user.is_doctor or not reservation.doctor_id == request.user.doctor:
            return Responses.getErrorResponse(status=status.HTTP_403_FORBIDDEN,
                                              error=_('your not allowed to perform this action'))
        if not data:
            return Responses.getErrorResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                              error=_('rejection reason field is required'))

        reservation.status = 'canceled'
        reservation.rejection_reason = data['rejection_reason']
        reservation.save()
        serializer = ConfirmReservationSerializer(reservation)
        email = reservation.patient_id.user.email
        send_reject_message(email, reservation.rejection_reason)
        return Responses.getResponse(status=status.HTTP_200_OK, data=serializer.data)
