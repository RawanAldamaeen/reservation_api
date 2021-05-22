from rest_framework import generics
from ..serializers.NewDoctorSerializer import CreateDoctorSerializer
from rest_framework.response import Response
from rest_framework import status
from ..models.doctor import Doctor


class DoctorCreate(generics.CreateAPIView):  # create new doctor view
    queryset = Doctor.objects.all()
    serializer_class = CreateDoctorSerializer

    def post(self, request, *args, **kwargs):   # perform post request
        serializer = CreateDoctorSerializer(data=request.data)

        # invalid data response
        if not serializer.is_valid():
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            data={"status": status.HTTP_422_UNPROCESSABLE_ENTITY, "data": {}, 'error': serializer.errors, 'meta': {}})
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data={"status": status.HTTP_201_CREATED, "data": serializer.data, 'meta': {}})
