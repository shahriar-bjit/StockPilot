from django.test import TestCase
from rest_framework.test import APITestCase

from apps.inventory.models import Category, Product
from apps.users.models import User, UserRole

# Create your tests here.

class ProductAPITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="testpass123",
            role=UserRole.ADMIN,
            is_staff=True,
        )
        self.auditor_user = User.objects.create_user(
            email="auditor@example.com",
            password="testpass123",
            role=UserRole.AUDITOR,
        )
        self.category = Category.objects.create(name="Office Supplies")

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin_user)

        payload = {
            "category": self.category.id,
            "name": "Printer Paper",
            "sku": "PP-001",
            "description": "A4 printer paper",
            "unit_price": "12.50",
            "stock_on_hand": 100,
            "reorder_level": 20,
            "is_active": True,
        }

        response = self.client.post("/api/products/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().created_by, self.admin_user)

    def test_auditor_cannot_create_product(self):
        self.client.force_authenticate(user=self.auditor_user)

        payload = {
            "category": self.category.id,
            "name": "Stapler",
            "sku": "ST-001",
            "description": "Office stapler",
            "unit_price": "8.00",
            "stock_on_hand": 10,
            "reorder_level": 2,
            "is_active": True,
        }

        response = self.client.post("/api/products/", payload, format="json")
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_view_products(self):
        Product.objects.create(
            category=self.category,
            name="Notebook",
            sku="NB-001",
            description="Ruled notebook",
            unit_price="5.00",
            stock_on_hand=50,
            reorder_level=10,
            is_active=True,
            created_by=self.admin_user,
        )

        self.client.force_authenticate(user=self.auditor_user)
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)