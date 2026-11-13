from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from .models import Lease, Payment, Property
from .serializers import LeaseSerializer, PaymentSerializer, PropertySerializer, UserProfileSerializer


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "OWNER"

class IsTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "TENANT"

class IsOwnerOfProperty(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or view it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the object is a Property or has a property owner
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'property'):
            return obj.property.owner == request.user
        return False

class IsTenantOfLease(permissions.BasePermission):
    """
    Custom permission to only allow the tenant assigned to a lease to access it.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'tenant'):
            return obj.tenant == request.user
        if hasattr(obj, 'lease'):
            return obj.lease.tenant == request.user
        return False


class OwnerPropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OwnerPropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsOwner, IsOwnerOfProperty]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class TenantLeaseView(generics.ListAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsTenant]

    def get_queryset(self):
        return Lease.objects.filter(
            tenant=self.request.user, status=Lease.Status.ACTIVE
        ).select_related("property")


class OwnerLeaseListView(generics.ListAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Lease.objects.filter(property__owner=self.request.user).select_related(
            "property", "tenant"
        )


class TenantPaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsTenant]

    def get_queryset(self):
        return Payment.objects.filter(lease__tenant=self.request.user).select_related(
            "lease"
        ).order_by("-payment_date", "-id")

    def perform_create(self, serializer):
        lease = Lease.objects.filter(
            tenant=self.request.user, status=Lease.Status.ACTIVE
        ).first()
        if lease is None:
            raise serializers.ValidationError(
                {"lease": "An active lease is required to submit a payment."}
            )
        serializer.save(lease=lease, status=Payment.Status.PENDING)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class OwnerPaymentStatusView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsOwner, IsOwnerOfProperty]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Payment.objects.filter(lease__property__owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        payment = self.get_object()
        new_status = request.data.get("status")
        allowed_statuses = {Payment.Status.APPROVED, Payment.Status.REJECTED}
        if new_status not in allowed_statuses:
            return Response(
                {"status": "Status must be APPROVED or REJECTED."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        payment.status = new_status
        payment.save(update_fields=["status"])
        return Response(self.get_serializer(payment).data)


class OwnerPendingPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Payment.objects.filter(
            lease__property__owner=self.request.user, 
            status=Payment.Status.PENDING
        ).select_related("lease__property").order_by("-payment_date")
