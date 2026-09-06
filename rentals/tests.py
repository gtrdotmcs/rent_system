from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Lease, Payment, Property


class RentalModelTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.owner = user_model.objects.create_user(
			username="owner",
			password="password",
			role=user_model.Role.OWNER,
		)
		self.tenant = user_model.objects.create_user(
			username="tenant",
			password="password",
			role=user_model.Role.TENANT,
		)
		self.property = Property.objects.create(
			owner=self.owner,
			name="Test Property",
			address="1 Test Street",
			city="Test City",
		)

	def test_payment_defaults_to_pending_and_validates_month(self):
		lease = Lease.objects.create(
			property=self.property,
			tenant=self.tenant,
			start_date=date(2026, 1, 1),
			monthly_rent=Decimal("1200.00"),
		)
		payment = Payment(
			lease=lease,
			amount_paid=Decimal("1200.00"),
			payment_date=date(2026, 1, 5),
			month=13,
			year=2026,
		)

		self.assertEqual(payment.status, Payment.Status.PENDING)
		with self.assertRaises(ValidationError):
			payment.full_clean()

	def test_property_cannot_have_two_active_leases(self):
		lease_data = {
			"property": self.property,
			"tenant": self.tenant,
			"start_date": date(2026, 1, 1),
			"monthly_rent": Decimal("1200.00"),
		}
		Lease.objects.create(**lease_data)

		with self.assertRaises(IntegrityError):
			with transaction.atomic():
				Lease.objects.create(**lease_data)


class Phase3WorkflowTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username="owner", password="password", role=user_model.Role.OWNER
        )
        self.tenant = user_model.objects.create_user(
            username="tenant", password="password", role=user_model.Role.TENANT
        )
        self.property = Property.objects.create(
            owner=self.owner, name="Test Prop", address="123 St", city="City"
        )
        self.lease = Lease.objects.create(
            property=self.property,
            tenant=self.tenant,
            start_date=date(2026, 1, 1),
            monthly_rent=Decimal("1000.00"),
            status=Lease.Status.ACTIVE
        )
        self.client = Client()

    def test_tenant_dashboard_access(self):
        self.client.login(username="tenant", password="password")
        response = self.client.get(reverse('tenant_lease_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Prop")

    def test_tenant_payment_submission(self):
        self.client.login(username="tenant", password="password")
        payload = {
            'amount_paid': '1000.00',
            'payment_date': '2026-08-23',
            'month': 8,
            'year': 2026
        }
        response = self.client.post(reverse('payment_submit'), data=payload)
        self.assertRedirects(response, reverse('payment_history'))
        
        payment = Payment.objects.get(month=8, year=2026)
        self.assertEqual(payment.status, Payment.Status.PENDING)
        self.assertEqual(payment.lease, self.lease)

    def test_owner_payment_approval(self):
        # Create a pending payment
        payment = Payment.objects.create(
            lease=self.lease,
            amount_paid=Decimal("1000.00"),
            payment_date=date(2026, 8, 23),
            month=8,
            year=2026,
            status=Payment.Status.PENDING
        )
        
        self.client.login(username="owner", password="password")
        # Approve payment
        response = self.client.get(reverse('payment_approve', args=[payment.pk, 'approve']))
        self.assertRedirects(response, reverse('owner_overview'))
        
        payment.refresh_from_db()
        self.assertEqual(payment.status, Payment.Status.APPROVED)

    def test_unauthorized_payment_approval(self):
        # Create another owner
        user_model = get_user_model()
        other_owner = user_model.objects.create_user(
            username="other", password="password", role=user_model.Role.OWNER
        )
        payment = Payment.objects.create(
            lease=self.lease,
            amount_paid=Decimal("1000.00"),
            payment_date=date(2026, 8, 23),
            month=8,
            year=2026
        )
        
        self.client.login(username="other", password="password")
        response = self.client.get(reverse('payment_approve', args=[payment.pk, 'approve']))
        self.assertEqual(response.status_code, 403)


class Phase4ApiTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username="api-owner", password="password", role=user_model.Role.OWNER
        )
        self.other_owner = user_model.objects.create_user(
            username="other-owner", password="password", role=user_model.Role.OWNER
        )
        self.tenant = user_model.objects.create_user(
            username="api-tenant", password="password", role=user_model.Role.TENANT
        )
        self.other_tenant = user_model.objects.create_user(
            username="other-tenant", password="password", role=user_model.Role.TENANT
        )
        self.property = Property.objects.create(
            owner=self.owner, name="API Property", address="1 API Street", city="API City"
        )
        self.other_property = Property.objects.create(
            owner=self.other_owner, name="Private Property", address="2 Private Street", city="Private City"
        )
        self.lease = Lease.objects.create(
            property=self.property,
            tenant=self.tenant,
            start_date=date(2026, 1, 1),
            monthly_rent=Decimal("1000.00"),
        )
        self.client = APIClient()

    def authenticate(self, username, password="password"):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_jwt_token_endpoint(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "api-tenant", "password": "password"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_tenant_can_read_only_own_active_lease_and_submit_payment(self):
        self.authenticate("api-tenant")
        lease_response = self.client.get(reverse("api-v1-tenant-lease"))
        self.assertEqual(lease_response.status_code, 200)
        self.assertEqual(len(lease_response.data), 1)
        self.assertEqual(lease_response.data[0]["id"], self.lease.id)

        payment_response = self.client.post(
            reverse("api-v1-tenant-payment-list"),
            {
                "amount_paid": "1000.00",
                "payment_date": "2026-08-23",
                "month": 8,
                "year": 2026,
            },
            format="json",
        )
        self.assertEqual(payment_response.status_code, 201)
        self.assertEqual(payment_response.data["status"], Payment.Status.PENDING)
        self.assertEqual(payment_response.data["lease"], self.lease.id)

    def test_owner_sees_only_owned_properties(self):
        self.authenticate("api-owner")
        response = self.client.get(reverse("api-v1-property-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [self.property.id])

    def test_owner_can_update_payment_status_but_other_owner_cannot(self):
        payment = Payment.objects.create(
            lease=self.lease,
            amount_paid=Decimal("1000.00"),
            payment_date=date(2026, 8, 23),
            month=8,
            year=2026,
        )
        self.authenticate("other-owner")
        forbidden = self.client.patch(
            reverse("api-v1-owner-payment-status", args=[payment.id]),
            {"status": Payment.Status.APPROVED},
            format="json",
        )
        self.assertEqual(forbidden.status_code, 404)

        self.authenticate("api-owner")
        approved = self.client.patch(
            reverse("api-v1-owner-payment-status", args=[payment.id]),
            {"status": Payment.Status.APPROVED},
            format="json",
        )
        self.assertEqual(approved.status_code, 200)
        payment.refresh_from_db()
        self.assertEqual(payment.status, Payment.Status.APPROVED)


class SecurityRegressionTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner1 = user_model.objects.create_user(username="owner1", password="password", role=user_model.Role.OWNER)
        self.owner2 = user_model.objects.create_user(username="owner2", password="password", role=user_model.Role.OWNER)
        self.tenant1 = user_model.objects.create_user(username="tenant1", password="password", role=user_model.Role.TENANT)
        self.tenant2 = user_model.objects.create_user(username="tenant2", password="password", role=user_model.Role.TENANT)
        
        self.prop1 = Property.objects.create(owner=self.owner1, name="Prop 1", address="Addr 1", city="City 1")
        self.prop2 = Property.objects.create(owner=self.owner2, name="Prop 2", address="Addr 2", city="City 2")
        
        self.lease1 = Lease.objects.create(
            property=self.prop1, tenant=self.tenant1, start_date=date(2026, 1, 1), monthly_rent=Decimal("1000.00")
        )
        self.lease2 = Lease.objects.create(
            property=self.prop2, tenant=self.tenant2, start_date=date(2026, 1, 1), monthly_rent=Decimal("1000.00")
        )
        
        self.payment1 = Payment.objects.create(
            lease=self.lease1, amount_paid=Decimal("1000.00"), payment_date=date(2026, 1, 5), month=1, year=2026
        )
        
        self.api_client = APIClient()

    def test_cross_owner_property_access_denied(self):
        # Owner 2 tries to update Owner 1's property
        self.api_client.force_authenticate(user=self.owner2)
        url = reverse('owner-property-detail', kwargs={'pk': self.prop1.pk})
        response = self.api_client.patch(url, {'name': 'Hacked Name'})
        self.assertEqual(response.status_code, 404) # get_queryset filters it out

    def test_cross_tenant_lease_access_denied(self):
        # Tenant 2 tries to view Tenant 1's lease
        self.api_client.force_authenticate(user=self.tenant2)
        # Note: The current TenantLeaseView uses ListAPIView with get_queryset
        url = reverse('tenant-lease-list')
        response = self.api_client.get(url)
        # Should only see their own lease, not lease1
        self.assertNotIn(str(self.lease1.id), response.data)

    def test_cross_owner_payment_approval_denied(self):
        # Owner 2 tries to approve Owner 1's payment
        self.api_client.force_authenticate(user=self.owner2)
        url = reverse('owner-payment-status', kwargs={'pk': self.payment1.pk})
        response = self.api_client.patch(url, {'status': 'APPROVED'})
        self.assertEqual(response.status_code, 404) # filtered by get_queryset

    def test_invalid_lease_dates_validation(self):
        with self.assertRaises(ValidationError):
            lease = Lease(
                property=self.prop1, tenant=self.tenant1, 
                start_date=date(2026, 1, 10), end_date=date(2026, 1, 1), 
                monthly_rent=Decimal("1000.00")
            )
            lease.full_clean()

    def test_duplicate_payment_validation(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                lease=self.lease1, amount_paid=Decimal("1000.00"), 
                payment_date=date(2026, 1, 6), month=1, year=2026
            )
            payment.full_clean()
