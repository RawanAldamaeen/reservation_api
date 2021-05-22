from rest_framework import authentication
from ..serializers.DoctorActivationserializer import ActivateDoctorSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from base.models.user import User


class DoctorActivation(APIView):  # activate doctor account view
    queryset = User.objects.all()
    serializer_class = ActivateDoctorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):    # perform put request
        data = request.data
        username = data['username']
        user = User.objects.get(username=username)
        active = data['is_active']

        # unauthorized users response
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"status": status.HTTP_403_FORBIDDEN, 'message': ('your not allowed to perform this action'), 'meta': {}})

        if not active:
            user.is_active = False
            user.save()

        user.is_active = True
        user.save()

        serializer = ActivateDoctorSerializer(user)
        return Response(status=status.HTTP_200_OK, data={"status": status.HTTP_200_OK, "data": serializer.data, 'meta': {}})
