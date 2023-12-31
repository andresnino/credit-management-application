# Generated by Django 4.2.3 on 2023-07-23 16:42

import apps.domain.constants.customers
import apps.domain.constants.loans
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(max_length=45)),
                (
                    "status",
                    models.CharField(
                        default=apps.domain.constants.customers.Status["ENABLED"],
                        max_length=15,
                    ),
                ),
                ("score", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "preapproved_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "db_table": "customers_customer",
                "db_table_comment": "Follow-up of all customers who are created",
                "unique_together": {("external_id",)},
            },
        ),
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(max_length=45)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        default=apps.domain.constants.loans.Status["ACTIVE"],
                        max_length=15,
                    ),
                ),
                ("contract_version", models.CharField(max_length=255, null=True)),
                ("maximum_payment_date", models.DateField()),
                ("taken_at", models.DateTimeField(auto_now_add=True)),
                ("outstanding", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="loans_loan",
                        to="manage_monitoring.customer",
                    ),
                ),
            ],
            options={
                "db_table": "loans_loan",
                "db_table_comment": "Store loans created by clients",
                "unique_together": {("external_id",)},
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(blank=True, max_length=45, null=True)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(max_length=15)),
                ("paid_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "customer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payments_payment",
                        to="manage_monitoring.customer",
                    ),
                ),
            ],
            options={
                "db_table": "payments_payment",
                "db_table_comment": "Receiving payments from customers",
                "unique_together": {("external_id",)},
            },
        ),
        migrations.CreateModel(
            name="PaymentDetail",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "loan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="details",
                        to="manage_monitoring.loan",
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="details",
                        to="manage_monitoring.payment",
                    ),
                ),
            ],
            options={
                "db_table": "payments_paymentdetail",
                "db_table_comment": "Store the payment detail, as one payment may cover one or several loans",
            },
        ),
    ]
