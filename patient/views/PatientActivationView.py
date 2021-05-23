import jwt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils.translation import gettext as _
from base.models.user import User


class VerifyUser(generics.GenericAPIView):  # Check & active patient account

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if user.is_active:
                return Response(status=status.HTTP_200_OK, data={"status": status.HTTP_200_OK,
                                                                 'data': {_('user'): _('User activated already')},
                                                                 'meta': {}})
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK, data={"status": status.HTTP_200_OK,
                                                         'data': {_('user'): _('Successfully activated')}, 'meta': {}})

        except jwt.ExpiredSignatureError as identifier:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"status": status.HTTP_404_NOT_FOUND, 'data': {},
                                                                    'error': _('Activation Expired'), 'meta': {}})
        except jwt.exceptions.DecodeError as identifier:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"status": status.HTTP_404_NOT_FOUND, 'data': {},
                                                                    'error': _('Invalid token'), 'meta': {}})

