from decimal import Decimal

from rest_framework.test import APITestCase

from apps.inventory.models import Category, Product
from apps.procurement.models import PurchaseOrder, PurchaseOrderStatus
from apps.suppliers.models import Supplier
from apps.users.models import User, UserRole


class PurchaseOrderAPITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            email="admin_po@example.com",
            password="testpass123",
            role=UserRole.ADMIN,
            is_staff=True,
        )
        self.procurement_user = User.objects.create_user(
            email="procurement_po@example.com",
            password="testpass123",
            role=UserRole.PROCUREMENT_OFFICER,
        )
        self.auditor_user = User.objects.create_user(
            email="auditor_po@example.com",
            password="testpass123",
            role=UserRole.AUDITOR,
        )

        self.category = Category.objects.create(name="Office Supplies")

        self.product = Product.objects.create(
            category=self.category,
            name="A4 Printer Paper",
            sku="PAPER-PO-001",
            description="A4 printer paper",
            unit_price=Decimal("12.50"),
            stock_on_hand=100,
            reorder_level=20,
            is_active=True,
            created_by=self.admin_user,
        )

        self.supplier = Supplier.objects.create(
            name="ABC Supplies Ltd",
            supplier_code="SUP-PO-001",
            email="po@abcsupplies.com",
            phone="0123456789",
            address="Dhaka, Bangladesh",
            contact_person="Rahim Uddin",
            is_active=True,
        )
        self.supplier.products.add(self.product)

    def test_procurement_officer_can_create_purchase_order(self):
        self.client.force_authenticate(user=self.procurement_user)

        payload = {
            "supplier": self.supplier.id,
            "expected_delivery_date": "2026-04-30",
            "remarks": "Urgent office supply order",
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 10,
                    "unit_price": "12.50",
                }
            ],
        }

        response = self.client.post("/api/purchase-orders/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(PurchaseOrder.objects.count(), 1)

        purchase_order = PurchaseOrder.objects.first()
        self.assertEqual(purchase_order.created_by, self.procurement_user)
        self.assertEqual(purchase_order.status, PurchaseOrderStatus.DRAFT)
        self.assertEqual(purchase_order.items.count(), 1)
        self.assertEqual(purchase_order.total_amount, Decimal("125.00"))

    def test_auditor_cannot_create_purchase_order(self):
        self.client.force_authenticate(user=self.auditor_user)

        payload = {
            "supplier": self.supplier.id,
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 5,
                    "unit_price": "12.50",
                }
            ],
        }

        response = self.client.post("/api/purchase-orders/", payload, format="json")

        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_view_purchase_orders(self):
        purchase_order = PurchaseOrder.objects.create(
            supplier=self.supplier,
            created_by=self.procurement_user,
        )
        purchase_order.items.create(
            product=self.product,
            quantity=2,
            unit_price=Decimal("12.50"),
        )

        self.client.force_authenticate(user=self.auditor_user)

        response = self.client.get("/api/purchase-orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_purchase_order_submit_and_approve_workflow(self):
        self.client.force_authenticate(user=self.procurement_user)

        payload = {
            "supplier": self.supplier.id,
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 4,
                    "unit_price": "12.50",
                }
            ],
        }

        create_response = self.client.post("/api/purchase-orders/", payload, format="json")
        self.assertEqual(create_response.status_code, 201)

        purchase_order_id = create_response.data["id"]

        submit_response = self.client.post(
            f"/api/purchase-orders/{purchase_order_id}/submit/"
        )
        self.assertEqual(submit_response.status_code, 200)
        self.assertEqual(submit_response.data["status"], PurchaseOrderStatus.SUBMITTED)

        self.client.force_authenticate(user=self.admin_user)

        approve_response = self.client.post(
            f"/api/purchase-orders/{purchase_order_id}/approve/"
        )
        self.assertEqual(approve_response.status_code, 200)
        self.assertEqual(approve_response.data["status"], PurchaseOrderStatus.APPROVED)

    def test_procurement_officer_cannot_approve_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(
            supplier=self.supplier,
            created_by=self.procurement_user,
            status=PurchaseOrderStatus.SUBMITTED,
        )
        purchase_order.items.create(
            product=self.product,
            quantity=3,
            unit_price=Decimal("12.50"),
        )

        self.client.force_authenticate(user=self.procurement_user)

        response = self.client.post(
            f"/api/purchase-orders/{purchase_order.id}/approve/"
        )

        self.assertEqual(response.status_code, 403)