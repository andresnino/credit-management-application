# Name:              serializers.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     22nd July of 2023
# Modification date: 24th July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

from rest_framework import serializers

from apps.manage_monitoring.models import Customer, Loan
from apps.manage_monitoring.utils.tools import enum_to_choices
from apps.domain.constants import (
    customers as cx_constants,
    loans as l_constants
)


class CustomerSerializer(serializers.Serializer):  # noqa
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    external_id = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=45
    )

    status = serializers.ChoiceField(
        required=False,
        choices=enum_to_choices(cx_constants.Status)
    )

    score = serializers.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2
    )

    preapproved_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `Customer` instance, given the validated data.
        """
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Customer` instance, given the
        validated data.
        """
        instance.external_id = validated_data.get(
            "external_id", instance.external_id
        )

        instance.score = validated_data.get("score", instance.score)
        instance.preapproved_at = validated_data.get(
            "preapproved_at", instance.preapproved_at
        )

        instance.save()
        return instance


class LoanSerializer(serializers.Serializer):  # noqa
    id = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    updated_at = serializers.DateTimeField(required=False, read_only=True)
    external_id = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=45
    )

    amount = serializers.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2
    )

    status = serializers.ChoiceField(
        required=False,
        choices=enum_to_choices(l_constants.Status)
    )
    contract_version = serializers.CharField(required=False, max_length=255)
    maximum_payment_date = serializers.DateField(
        required=True,
        allow_null=False
    )

    taken_at = serializers.DateTimeField(
        required=False,
        allow_null=False,
        read_only=True
    )

    customer_id = serializers.CharField(
        required=False,
        allow_null=False
    )

    outstanding = serializers.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2
    )

    def create(self, validated_data):
        """
        Create and return a new `Loan` instance, given the validated data.
        """

        return Loan.objects.create(**validated_data)
