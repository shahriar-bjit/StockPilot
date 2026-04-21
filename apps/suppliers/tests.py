from django.test import TestCase
from rest_framework.test import APITestCase
from apps.inventory.models import Category, Product
from apps.suppliers.models import Supplier
from apps.users.models import User, UserRole

# Create your tests here.

class SupplierAPITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            email="admin_supplier@example.com",
            password="testpass123",
            role=UserRole.ADMIN,
            is_staff=True,
        )
        self.procurement_user = User.objects.create_user(
            email="procurement@example.com",
            password="testpass123",
            role=UserRole.PROCUREMENT_OFFICER,
        )
        self.auditor_user = User.objects.create_user(
            email="auditor_supplier@example.com",
            password="testpass123",
            role=UserRole.AUDITOR,
        )

        self.category = Category.objects.create(name="Office Supplies")
        self.product = Product.objects.create(
            category=self.category,
            name="Printer Paper",
            sku="PP-100",
            description="A4 paper",
            unit_price="12.50",
            stock_on_hand=100,
            reorder_level=20,
            is_active=True,
            created_by=self.admin_user,
        )

    def test_procurement_officer_can_create_supplier(self):
        self.client.force_authenticate(user=self.procurement_user)

        payload = {
            "name": "ABC Supplies Ltd",
            "supplier_code": "SUP-001",
            "email": "contact@abcsupplies.com",
            "phone": "0123456789",
            "address": "Dhaka, Bangladesh",
            "contact_person": "Rahim Uddin",
            "is_active": True,
            "products": [self.product.id],
        }

        response = self.client.post("/api/suppliers/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(Supplier.objects.first().products.count(), 1)

    def test_auditor_cannot_create_supplier(self):
        self.client.force_authenticate(user=self.auditor_user)

        payload = {
            "name": "XYZ Traders",
            "supplier_code": "SUP-002",
            "email": "info@xyztraders.com",
            "products": [self.product.id],
        }

        response = self.client.post("/api/suppliers/", payload, format="json")
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_view_suppliers(self):
        supplier = Supplier.objects.create(
            name="View Supplier",
            supplier_code="SUP-003",
            email="view@supplier.com",
            is_active=True,
        )
        supplier.products.add(self.product)

        self.client.force_authenticate(user=self.auditor_user)
        response = self.client.get("/api/suppliers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)