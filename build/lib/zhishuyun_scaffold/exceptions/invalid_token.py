from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _(
        'The token is invalid, please make sure your token is correct.')
    default_code = 'invalid_token'
