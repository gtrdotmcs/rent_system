from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('leases/create/', views.lease_create, name='lease_create'),
    path('overview/', views.owner_overview, name='owner_overview'),
    path('tenant/dashboard/', views.tenant_lease_dashboard, name='tenant_lease_dashboard'),
    path('tenant/payment/submit/', views.payment_submit, name='payment_submit'),
    path('tenant/payment/history/', views.payment_history, name='payment_history'),
    path('payment/<int:pk>/<str:action>/', views.payment_approve, name='payment_approve'),
]
