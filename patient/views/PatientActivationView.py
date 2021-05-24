import jwt
from rest_framework import generics
from rest_framework import status
from django.conf import settings
from django.utils.translation import gettext as _
from base.models.user import User
from reservations.response import Responses


class VerifyUser(generics.GenericAPIView):  # Check & active patient account

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if user.is_active:
                return Responses.getResponse(status=status.HTTP_200_OK, data={_('user'): _('User activated already')})

            user.is_active = True
            user.save()
            return Responses.getResponse(status=status.HTTP_200_OK, data={_('user'): _('Successfully activated')})

        except jwt.ExpiredSignatureError as identifier:
            return Responses.getErrorResponse(status=status.HTTP_404_NOT_FOUND, error=_('Activation Expired'))

        except jwt.exceptions.DecodeError as identifier:
            return Responses.getErrorResponse(status=status.HTTP_404_NOT_FOUND, error=_('Invalid token'))


