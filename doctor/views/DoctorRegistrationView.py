from rest_framework import generics
from ..serializers.NewDoctorSerializer import CreateDoctorSerializer
from rest_framework import status
from ..models.doctor import Doctor
from reservations.response import Responses


class DoctorCreate(generics.CreateAPIView):  # create new doctor view
    queryset = Doctor.objects.all()
    serializer_class = CreateDoctorSerializer

    def post(self, request, *args, **kwargs):   # perform post request
        serializer = CreateDoctorSerializer(data=request.data)

        # invalid data response
        if not serializer.is_valid():
            return Responses.getErrorResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, error=serializer.errors)

        serializer.save()
        return Responses.getResponse(status=status.HTTP_201_CREATED, data=serializer.data)
