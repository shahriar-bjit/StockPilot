from django.core.management.base import BaseCommand

from apps.inventory.models import Category, Product
from apps.users.models import User, UserRole


class Command(BaseCommand):
    help = "Seed inventory demo data"

    def handle(self, *args, **options):
        admin_user, _ = User.objects.get_or_create(
            email="admin_seed@example.com",
            defaults={
                "role": UserRole.ADMIN,
                "is_staff": True,
                "is_superuser": False,
            },
        )
        if not admin_user.has_usable_password():
            admin_user.set_password("testpass123")
            admin_user.save()

        office, _ = Category.objects.get_or_create(name="Office Supplies")
        accessories, _ = Category.objects.get_or_create(name="Computer Accessories")

        Product.objects.get_or_create(
            sku="OPS-PAPER-001",
            defaults={
                "category": office,
                "name": "A4 Printer Paper",
                "description": "High-quality A4 printer paper for office printing and documentation.",
                "unit_price": 12.50,
                "stock_on_hand": 100,
                "reorder_level": 20,
                "is_active": True,
                "created_by": admin_user,
            },
        )

        Product.objects.get_or_create(
            sku="ACC-KEY-001",
            defaults={
                "category": accessories,
                "name": "USB Keyboard",
                "description": "Standard wired USB keyboard for office workstations.",
                "unit_price": 18.00,
                "stock_on_hand": 5,
                "reorder_level": 10,
                "is_active": True,
                "created_by": admin_user,
            },
        )

        self.stdout.write(self.style.SUCCESS("Inventory demo data seeded successfully."))