# Name:              permissions.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     24th July of 2023
# Modification date: 24th July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

from django.conf import settings
from rest_framework.permissions import BasePermission


class CheckApiKeyAuth(BasePermission):
    def has_permission(self, request, view):
        # API-KEY should be in request headers to authenticate requests
        api_key_secret = request.META.get("HTTP_API_KEY")
        return api_key_secret == settings.API_KEY_SECRET
