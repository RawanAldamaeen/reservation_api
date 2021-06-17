from rest_framework import generics
from ..serializers.CreateShiftSerializer import CreateShiftSerializer
from rest_framework import status
from ..models.shifts import Shift
from django.utils.translation import gettext as _
from reservations.response import Responses


class ShiftCreateView(generics.CreateAPIView):  # create new shift view
    queryset = Shift.objects.all()
    serializer_class = CreateShiftSerializer

    def post(self, request, *args, **kwargs):

        # check if user is doctor
        if request.user.is_anonymous or not request.user.is_doctor:
            return Responses.getErrorResponse(status=status.HTTP_403_FORBIDDEN,
                                              error=_('your not allowed to perform this action'))

        serializer = CreateShiftSerializer(data=request.data)
        if not serializer.is_valid():
            return Responses.getErrorResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                              error=serializer.errors)

        serializer.save(doctor_id=request.user.doctor)

        return Responses.getResponse(status=status.HTTP_201_CREATED, data=serializer.data)

