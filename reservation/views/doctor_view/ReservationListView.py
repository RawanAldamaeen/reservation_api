from rest_framework import generics, status, pagination
from rest_framework.filters import SearchFilter
from reservation.serializers.doctor_serializer.ReservationListSerializer import ReservationListSerializer
from reservations.response import Responses
from reservation.models.reservation import Reservation
from django.utils.translation import gettext as _


class ReservationsListPagination(pagination.PageNumberPagination):  # Reservations list pagination settings
    default_limit = 10
    max_limit = 20

    def get_paginated_response(self, data):
        search = self.request.query_params.get('search')
        if search is None:
            search = ''
        meta = {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'search': search,
        }

        return Responses.getResponse(status=status.HTTP_200_OK, data=data, meta=meta)


class ReservationsListView(generics.ListAPIView):  # All reservations list view
    queryset = Reservation.objects.all()
    serializer_class = ReservationListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['patient_id', 'status']
    pagination_class = ReservationsListPagination

    def list(self, request, *args, **kwargs):
        # check if user is doctor
        if request.user.is_anonymous or not request.user.is_doctor:
            return Responses.getErrorResponse(status=status.HTTP_403_FORBIDDEN,
                                              error=_('your not allowed to perform this action'))

        patient_list = Reservation.objects.all().filter(doctor_id=request.user.doctor)
        page = self.paginate_queryset(patient_list)
        serializer = ReservationListSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)