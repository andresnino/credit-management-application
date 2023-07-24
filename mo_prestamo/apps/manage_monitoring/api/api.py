# Name:              api.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     22nd July of 2023
# Modification date: 24th July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField
from django.http import Http404

from apps.manage_monitoring.models import Customer, Loan
from apps.domain.constants import loans as l_constants
from apps.manage_monitoring.api.serializers import (
    CustomerSerializer, LoanSerializer
)


@api_view(["GET", "POST", "PUT"])
#  @permission_classes((CheckApiKeyAuth,))
def customer_api_view(request, pk=None):
    """Create and request customer information"""

    response_fields = [
        "id",
        "external_id",
        "status",
        "score",
        "preapproved_at"
    ]

    def get_object(pk):  # noqa
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    if request.method == "GET":
        customer = get_object(pk)
        serializer = CustomerSerializer(customer)
        data = serializer.data

        response = {key: data.get(key) for key in response_fields}
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = CustomerSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()

            data, response = serializer.data, []
            for item in data:
                values = {key: item.get(key) for key in response_fields}
                response.append(values)

            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        customer = get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()

            data = serializer.data

            response = {key: data.get(key) for key in response_fields}
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def customer_balance_api_view(request, pk=None):
    """
    Consult customer balance sheet.

    Total debt, is the sum of the outstanding of all  loans active and pending.
    Amount available, is the score minus the total debt.
    """

    def get_object(pk):  # noqa
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    if request.method == "GET":
        customer = get_object(pk)
        customer_serializer = CustomerSerializer(customer)
        customer_data = customer_serializer.data

        balance = Loan.objects.filter(
            customer_id=pk,
            status__in=[l_constants.Status.ACTIVE, l_constants.Status.PENDING]
        )

        total_debt = balance.aggregate(
            debt=Coalesce(Sum("amount"), 0.0, output_field=DecimalField())
        )

        total_debt = float(total_debt.get("debt", 0.0))

        external_id = customer_data.get("external_id")
        score = customer_data.get("score", 0.0)
        available_amount = float(score) - total_debt

        response = {
            "id": pk,
            "external_id": external_id,
            "score": score,
            "available_amount": available_amount,
            "total_debt": total_debt
        }

        return Response(response, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def loan_api_view(request, pk=None):
    """Create and request loan information"""

    response_fields = [
        "id",
        "external_id",
        "customer_id",
        "amount",
        "outstanding",
        "status"
    ]

    def get_object(model, pk):  # noqa
        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise Http404

    if request.method == "GET":
        loan = get_object(Loan, pk)
        serializer = LoanSerializer(loan)

        data = serializer.data

        response = {key: data.get(key) for key in response_fields}
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == "POST":
        data = request.data

        customer_id = data.get("customer_id")
        loan_amount = data.get("amount")

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            msg = {
                "detail": "customer_id not found. All loans must be "
                          "associated with a specific Customer."
            }

            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        customer_serializer = CustomerSerializer(customer)
        customer_data = customer_serializer.data

        # Get total debt

        balance = Loan.objects.filter(
            customer_id=pk,
            status__in=[l_constants.Status.ACTIVE, l_constants.Status.PENDING]
        )

        total_debt = balance.aggregate(
            debt=Coalesce(Sum("amount"), 0.0, output_field=DecimalField())
        )

        total_debt = float(total_debt["debt"])

        available_amount = float(customer_data.get("score")) - total_debt
        if available_amount < float(loan_amount):
            msg = {"detail": "Your available score is lower than the "
                             "requested amount"}
            return Response(msg, status=status.HTTP_200_OK)

        # Create loan

        loan_serializer = LoanSerializer(data=data)
        if loan_serializer.is_valid():
            loan_serializer.save()

            data = loan_serializer.data
            response = {key: data.get(key) for key in response_fields}

            return Response(
                data=response,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=loan_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def loan_detail_api_view(request, pk=None):
    """Get loans by customer"""

    response_fields = [
        "id",
        "external_id",
        "customer_id",
        "amount",
        "outstanding",
        "status"
    ]

    def get_object(model, pk):  # noqa
        try:
            return model.objects.filter(customer_id=pk)
        except model.DoesNotExist:
            raise Http404

    if request.method == "GET":
        loan = get_object(Loan, pk)
        serializer = LoanSerializer(loan, many=True)

        data, response = serializer.data, []
        for item in data:
            values = {key: item.get(key) for key in response_fields}
            response.append(values)

        return Response(response, status=status.HTTP_200_OK)
