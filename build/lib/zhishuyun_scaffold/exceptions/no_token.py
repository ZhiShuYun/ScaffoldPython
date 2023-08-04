from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class NoTokenException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('No token specified in url query.')
    default_code = 'no_token'
