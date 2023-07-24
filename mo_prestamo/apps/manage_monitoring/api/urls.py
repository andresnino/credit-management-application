# Name:              urls.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     22nd July of 2023
# Modification date: 24th July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from apps.manage_monitoring.api.api import (
    customer_api_view, customer_balance_api_view, loan_api_view,
    loan_detail_api_view
)

urlpatterns = [
    path(
        route="customer/",
        view=customer_api_view,
        name="customer_api_view"
    ),
    path(
        route="customer/<str:pk>/",
        view=customer_api_view,
        name="customer_api_view"
    ),
    path(
        route="customer/balance/<str:pk>/",
        view=customer_balance_api_view,
        name="customer_balance_api_view"
    ),
    path(
        route="loan/",
        view=loan_api_view,
        name="loan_api_view"
    ),
    path(
        route="loan/<str:pk>/",
        view=loan_api_view,
        name="loan_api_view"
    ),
    path(
        route="loan/detail/<str:pk>/",
        view=loan_detail_api_view,
        name="loan_detail_pi_view"
    )
]

urlpatterns = format_suffix_patterns(urlpatterns)
