from rest_framework import generics
from rest_framework.authtoken.models import Token

from ..serializers.DoctorLoginSerializer import DoctorLoginSerializers
from django.contrib.auth.models import update_last_login
from rest_framework import status
from base.models.user import User
from reservations.response import Responses


class DoctorLoginView(generics.GenericAPIView):    # Doctor login view
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = DoctorLoginSerializers(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Responses.getErrorResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, error=serializer.errors)

        user = serializer.validated_data['user']
        update_last_login(None, user)
        token, created = Token.objects.get_or_create(user=user)
        return Responses.getResponse(status=status.HTTP_200_OK, data={"Token": token.key})