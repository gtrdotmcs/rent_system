from rest_framework import serializers
from django.conf import settings

from .models import Lease, Payment, Property, User


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Property
        fields = ["id", "owner", "name", "address", "city", "description"]


class LeaseSerializer(serializers.ModelSerializer):
    property_name = serializers.ReadOnlyField(source="property.name")
    tenant = serializers.ReadOnlyField(source="tenant.username")

    class Meta:
        model = Lease
        fields = [
            "id",
            "property",
            "property_name",
            "tenant",
            "start_date",
            "end_date",
            "monthly_rent",
            "status",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    lease = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "lease",
            "amount_paid",
            "payment_date",
            "month",
            "year",
            "status",
        ]

    def validate_amount_paid(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount paid must be positive.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "role"]
