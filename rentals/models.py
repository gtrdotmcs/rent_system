from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

class Property(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties",
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Lease(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        EXPIRED = "EXPIRED", "Expired"
        TERMINATED = "TERMINATED", "Terminated"

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="leases",
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leases",
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property"],
                condition=Q(status="ACTIVE"),
                name="one_active_lease_per_property",
            ),
        ]

    def __str__(self):
        return f"{self.property} - {self.tenant}"


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    lease = models.ForeignKey(
        Lease,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    month = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    year = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount_paid <= 0:
            raise ValidationError("Amount paid must be positive.")
        
        # Prevent duplicate payments for the same lease, month, and year
        duplicate = Payment.objects.filter(
            lease=self.lease, 
            month=self.month, 
            year=self.year
        ).exclude(pk=self.pk)
        if duplicate.exists():
            raise ValidationError("A payment for this month and year has already been submitted for this lease.")

    def __str__(self):
        return f"{self.lease} - {self.month}/{self.year}"
