from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class TokenMismatchedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('token and api does not match.')
    default_code = 'token_mismatched'
