# Name:              error_handling.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     22nd July of 2023
# Modification date: 24th July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

from rest_framework.views import exception_handler
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code
    elif isinstance(exc, IntegrityError):
        data = {
            "detail": "It seems there is a conflict between the data you are "
                      "trying to save and your current data. Please review "
                      "your entries and try again."
        }

        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return response
