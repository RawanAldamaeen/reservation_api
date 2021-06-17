from rest_framework import generics, status, pagination
from rest_framework.filters import SearchFilter
from reservation.serializers.patient_serializer import DoctorsListSerializer
from doctor.models.doctor import Doctor
from reservations.response import Responses
from django.utils.translation import gettext as _


class DoctorsListPagination(pagination.PageNumberPagination):  # doctors list pagination settings
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


class DoctorsListView(generics.ListAPIView):  # All doctors list view
    queryset = Doctor.objects.all()
    serializer_class = DoctorsListSerializer
    filter_backends = [SearchFilter]
    search_fields = ('name',)
    pagination_class = DoctorsListPagination

    def list(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()
        page = self.paginate_queryset(doctors)

        # check if user is patient
        if request.user.is_anonymous or not request.user.is_patient:
            return Responses.getErrorResponse(status=status.HTTP_403_FORBIDDEN,
                                              error=_('your not allowed to perform this action'))
        # check user language
        language = request.user.language
        if language == 'ar':
            serializer = DoctorsListSerializer.DoctorsListARSerializer(page, many=True)
        else:
            serializer = DoctorsListSerializer.DoctorsListSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)
