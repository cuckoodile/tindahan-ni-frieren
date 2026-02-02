from django.utils import timezone
from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = "Seed Users with admins (admin and fern) and 10 random customers."

    def handle(self, *args, **options):
        seeder = Seed.seeder(locale='en_PH')

        self.stdout.write(self.style.NOTICE("Starting user seeding..."))

        # ── 1. Groups ────────────────────────────────────────────────────────
        def create_group(name: str, perm_codes=None):
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(f"→ Created group: {name}")
            else:
                self.stdout.write(f"→ Group already exists: {name}")

            if perm_codes:
                permissions = Permission.objects.filter(codename__in=perm_codes)
                group.permissions.set(permissions)
                self.stdout.write(f"   Added {len(permissions)} permissions")

            return group



        admin_group = create_group('admin', Permission.objects.all())

        customer_group = create_group('customer')


        # ── 2. Super Users ────────────────────────────────────────────────────────
        seeder.add_entity(CustomUser, 1, {
            'username': 'admin',
            'password': make_password('admin'),
            'phone_number': lambda x: '+639' + seeder.faker.msisdn()[4:],
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'date_joined': timezone.now(),
            'last_login': None,
        })

        seeder.add_entity(CustomUser, 1, {
            'username': 'fern',
            'password': make_password('fern'),
            'phone_number': lambda x: '+639' + seeder.faker.msisdn()[4:],
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'date_joined': timezone.now(),
            'last_login': None,
        })


        # ── 3. Random Customers ────────────────────────────────────────────────────────
        seeder.add_entity(CustomUser, 10, {
            'username': lambda x: seeder.faker.user_name(),
            'password': make_password('Pass123!'),
            'phone_number': lambda x: '+639' + seeder.faker.msisdn()[4:],
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'date_joined': timezone.now(),
            'last_login': None,
        })


        # ── Execute ──────────────────────────────────────────────────────────
        try:
            inserted_pks = seeder.execute()
            self.stdout.write(self.style.SUCCESS(
                f"Seeding complete! Inserted PKs: {inserted_pks}"
            ))

            # ── Set M2M ───────────────────────────────────────────────────────
            # Admins
            admin_user = CustomUser.objects.get(username='admin')
            fern_user = CustomUser.objects.get(username='fern')

            admin_user.groups.set([admin_group])
            fern_user.groups.set([admin_group])

            # Customers
            customers = CustomUser.objects.exclude(username__in=['admin', 'fern'])

            for user in customers:
                user.groups.set([customer_group])

            self.stdout.write(self.style.SUCCESS('Groups assigned successfully.'))


        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Seeding failed: {exc}"))
            raise  # or handle gracefully

        