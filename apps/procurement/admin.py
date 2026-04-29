from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem

# Register your models here.

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    readonly_fields = ("line_total", "created_at", "updated_at")


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        "po_number",
        "supplier",
        "status",
        "created_by",
        "approved_by",
        "order_date",
        "expected_delivery_date",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "supplier", "order_date", "created_at")
    search_fields = ("po_number", "supplier__name", "created_by__email")
    readonly_fields = (
        "po_number",
        "total_amount",
        "submitted_at",
        "approved_at",
        "rejected_at",
        "completed_at",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = ("supplier", "created_by", "approved_by")
    inlines = [PurchaseOrderItemInline]


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_order",
        "product",
        "quantity",
        "unit_price",
        "line_total",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "purchase_order__po_number",
        "product__name",
        "product__sku",
    )
    readonly_fields = ("line_total", "created_at", "updated_at")
    autocomplete_fields = ("purchase_order", "product")