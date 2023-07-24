# Name:              models.py
# Author:            Mo Tecnologias
# Developers:        Miguel Andres Garcia Niño
# Creation date:     22nd July of 2023
# Modification date: 24th July of 2023
# Copyright:         (c) 2016 by Mo Tecnologias, 2023

import uuid

from django.db import models
from django.utils import timezone

from apps.manage_monitoring.utils.tools import enum_to_choices
from apps.domain.constants import (
    customers as cx_constants,
    loans as l_constants,
    payments as payt_constants
)


class BaseModelUUID(models.Model):
    """
    Base Model to be implemented in all models.
    The difference with the BaseModel is the ID or PK is an uuid.

    Attributes:
        identifier: A UUID4 value to identify an object.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class Customer(BaseModelUUID):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=45)
    status = models.CharField(
        max_length=15,
        choices=enum_to_choices(cx_constants.Status),
        default=cx_constants.Status.ENABLED
    )

    score = models.DecimalField(max_digits=10, decimal_places=2)
    preapproved_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "customers_customer"
        db_table_comment = "Follow-up of all customers who are created"
        unique_together = ("external_id",)

    def __str__(self):
        return str(self.id)


class Loan(BaseModelUUID):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=45, blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=15,
        choices=enum_to_choices(l_constants.Status),
        default=l_constants.Status.ACTIVE
    )

    contract_version = models.CharField(max_length=255, null=True)
    maximum_payment_date = models.DateField(blank=False, null=False)
    taken_at = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="loans_loan"
    )

    outstanding = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "loans_loan"
        db_table_comment = "Store loans created by clients"
        unique_together = ("external_id",)

    def __str__(self):
        return str(self.id)

    @property
    def is_active(self) -> bool:
        return self.status == l_constants.Status.ACTIVE


class Payment(BaseModelUUID):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=45, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=15,
        choices=enum_to_choices(payt_constants.Status)
    )

    paid_at = models.DateTimeField(default=timezone.now)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.PROTECT,
        related_name="payments_payment"
    )

    class Meta:
        db_table = "payments_payment"
        db_table_comment = "Receiving payments from customers"
        unique_together = ("external_id",)

    def __str__(self):
        return str(self.id)


class PaymentDetail(BaseModelUUID):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan = models.ForeignKey(
        Loan, on_delete=models.PROTECT, related_name="details"
    )

    payment = models.ForeignKey(
        Payment, on_delete=models.PROTECT, related_name="details"
    )

    class Meta:
        db_table = "payments_paymentdetail"
        db_table_comment = "Store the payment detail, as one payment may " \
                           "cover one or several loans"

    def __str__(self):
        return str(self.id)
