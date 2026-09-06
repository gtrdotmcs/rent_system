from django.contrib import admin

from .models import Lease, Payment, Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
	list_display = ("name", "city", "owner")
	list_filter = ("city",)
	search_fields = ("name", "address", "city", "owner__username")


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
	list_display = ("property", "tenant", "monthly_rent", "start_date", "end_date", "status")
	list_filter = ("status",)
	search_fields = ("property__name", "tenant__username")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ("lease", "amount_paid", "payment_date", "month", "year", "status")
	list_filter = ("status", "year")
	search_fields = ("lease__property__name", "lease__tenant__username")
