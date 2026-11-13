from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rentals.api import (
    OwnerLeaseListView,
    OwnerPaymentStatusView,
    OwnerPendingPaymentsView,
    OwnerPropertyDetailView,
    OwnerPropertyListCreateView,
    TenantLeaseView,
    TenantPaymentListCreateView,
    UserProfileView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("properties/", OwnerPropertyListCreateView.as_view(), name="api-v1-property-list"),
    path("properties/<int:pk>/", OwnerPropertyDetailView.as_view(), name="api-v1-property-detail"),
    path("owner/leases/", OwnerLeaseListView.as_view(), name="api-v1-owner-lease-list"),
    path("tenant/lease/", TenantLeaseView.as_view(), name="api-v1-tenant-lease"),
    path("tenant/payments/", TenantPaymentListCreateView.as_view(), name="api-v1-tenant-payment-list"),
    path("me/", UserProfileView.as_view(), name="api-v1-me"),
    path("owner/payments/pending/", OwnerPendingPaymentsView.as_view(), name="api-v1-owner-payments-pending"),
    path("owner/payments/<int:pk>/status/", OwnerPaymentStatusView.as_view(), name="api-v1-owner-payment-status"),
]
