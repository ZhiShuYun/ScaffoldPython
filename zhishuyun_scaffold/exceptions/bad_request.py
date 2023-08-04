from rest_framework.exceptions import APIException
from rest_framework import status


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_request'
