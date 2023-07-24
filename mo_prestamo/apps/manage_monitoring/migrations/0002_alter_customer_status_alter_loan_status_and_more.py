# Generated by Django 4.2.3 on 2023-07-24 19:38

import apps.domain.constants.customers
import apps.domain.constants.loans
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manage_monitoring", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="status",
            field=models.CharField(
                choices=[("enabled", "ENABLED"), ("disabled", "DISABLED")],
                default=apps.domain.constants.customers.Status["ENABLED"],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "PENDING"),
                    ("active", "ACTIVE"),
                    ("rejected", "REJECTED"),
                    ("paid", "PAID"),
                ],
                default=apps.domain.constants.loans.Status["ACTIVE"],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[("completed", "COMPLETED"), ("rejected", "REJECTED")],
                max_length=15,
            ),
        ),
    ]