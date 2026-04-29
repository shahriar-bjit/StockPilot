from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings
from apps.inventory.models import Product
from apps.suppliers.models import Supplier

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PurchaseOrderStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    COMPLETED = "completed", "Completed"

class PurchaseOrder(TimeStampedModel):
    po_number = models.CharField(max_length=20, unique=True, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_purchase_orders')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='approved_purchase_orders', null=True, blank=True)
    status = models.CharField(max_length=20, choices=PurchaseOrderStatus.choices, default=PurchaseOrderStatus.DRAFT, db_index=True)
    order_date = models.DateField(default=timezone.localdate)
    expected_delivery_date = models.DateField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["po_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["supplier"]),
            models.Index(fields=["created_by"]),
        ]

    def __str__(self):
        return f"PO {self.po_number} - {self.supplier.name} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            self.po_number = self.generate_po_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_po_number():
        today = timezone.localdate()
        prefix = f"PO-{today.strftime('%Y%m')}"
        count = PurchaseOrder.objects.filter(po_number__startswith=prefix).count() + 1
        return f"{prefix}-{count:04d}"
    
    def recalculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=["total_amount", "updated_at"])


class PurchaseOrderItem(TimeStampedModel):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_order_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), editable=False,)

    class Meta:
        ordering = ["id"]
        unique_together = ("purchase_order", "product")

    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.sku}"
    
    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.purchase_order.recalculate_total()

    def delete(self, *args, **kwargs):
        purchase_order = self.purchase_order
        super().delete(*args, **kwargs)
        purchase_order.recalculate_total()