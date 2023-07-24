from django.contrib import admin
from apps.manage_monitoring.models import (
    Customer, Loan, Payment, PaymentDetail
)

admin.site.register([Customer, Loan, Payment, PaymentDetail])
