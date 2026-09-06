from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rentals.models import Property, Lease
from decimal import Decimal
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial test data for the rent system'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. Create Super Admin
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser(
                username='superadmin',
                email='admin@example.com',
                password='adminpassword123',
                role=User.Role.SUPER_ADMIN
            )
            self.stdout.write('Created Super Admin: superadmin / adminpassword123')

        # 2. Create Owner
        if not User.objects.filter(username='owner1').exists():
            User.objects.create_user(
                username='owner1',
                email='owner1@example.com',
                password='ownerpassword123',
                first_name='John',
                last_name='Owner',
                role=User.Role.OWNER
            )
            self.stdout.write('Created Owner: owner1 / ownerpassword123')

        # 3. Create Tenant
        if not User.objects.filter(username='tenant1').exists():
            User.objects.create_user(
                username='tenant1',
                email='tenant1@example.com',
                password='tenantpassword123',
                first_name='Jane',
                last_name='Tenant',
                role=User.Role.TENANT
            )
            self.stdout.write('Created Tenant: tenant1 / tenantpassword123')

        # Get the users
        owner = User.objects.get(username='owner1')
        tenant = User.objects.get(username='tenant1')

        # 4. Create Property
        property_obj, created = Property.objects.get_or_create(
            name='Sunset Apartments',
            defaults={
                'owner': owner,
                'address': '123 Sunset Blvd',
                'city': 'Los Angeles',
                'description': 'A beautiful apartment with a view of the sunset.'
            }
        )
        if created:
            self.stdout.write('Created Property: Sunset Apartments')

        # 5. Create Lease
        lease, created = Lease.objects.get_or_create(
            property=property_obj,
            tenant=tenant,
            defaults={
                'start_date': date(2026, 1, 1),
                'end_date': date(2026, 12, 31),
                'monthly_rent': Decimal('1200.00'),
                'status': 'ACTIVE'
            }
        )
        if created:
            self.stdout.write('Created Active Lease for tenant1')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
