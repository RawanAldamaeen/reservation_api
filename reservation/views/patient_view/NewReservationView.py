from rest_framework import generics
from reservation.serializers.patient_serializer.NewReservationSerializer import NewReservationView
from rest_framework import status
from reservation.models.reservation import Reservation
from django.utils.translation import gettext as _
from reservations.response import Responses


class ReservationCreateView(generics.CreateAPIView):  # create new reservation view
    queryset = Reservation.objects.all()
    serializer_class = NewReservationView

    def post(self, request, *args, **kwargs):
        serializer = NewReservationView(data=request.data)
        # check if user is patient
        if request.user.is_anonymous or not request.user.is_patient:
            return Responses.getErrorResponse(status=status.HTTP_403_FORBIDDEN,
                                              error=_('your not allowed to perform this action'))

        if not serializer.is_valid():
            return Responses.getErrorResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, error=serializer.errors)

        serializer.save(patient_id=request.user.patient)

        return Responses.getResponse(status=status.HTTP_201_CREATED, data=serializer.data)
