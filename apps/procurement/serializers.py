from django.db import transaction
from rest_framework import serializers

from apps.inventory.models import Product
from apps.suppliers.models import Supplier

from .models import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_sku = serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = (
            "id",
            "product",
            "product_name",
            "product_sku",
            "quantity",
            "unit_price",
            "line_total",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "product_name",
            "product_sku",
            "line_total",
            "created_at",
            "updated_at",
        )

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)
    approved_by_email = serializers.CharField(source="approved_by.email", read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = (
            "id",
            "po_number",
            "supplier",
            "supplier_name",
            "created_by",
            "created_by_email",
            "approved_by",
            "approved_by_email",
            "status",
            "order_date",
            "expected_delivery_date",
            "submitted_at",
            "approved_at",
            "rejected_at",
            "completed_at",
            "remarks",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "po_number",
            "created_by",
            "created_by_email",
            "approved_by",
            "approved_by_email",
            "status",
            "submitted_at",
            "approved_at",
            "rejected_at",
            "completed_at",
            "total_amount",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        items = attrs.get("items")

        if self.instance is None and not items:
            raise serializers.ValidationError({"items": "At least one item is required."})

        supplier = attrs.get("supplier", getattr(self.instance, "supplier", None))
        if supplier and not supplier.is_active:
            raise serializers.ValidationError({"supplier": "Selected supplier is inactive."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        request = self.context.get("request")

        purchase_order = PurchaseOrder.objects.create(
            created_by=request.user,
            **validated_data,
        )

        for item_data in items_data:
            PurchaseOrderItem.objects.create(
                purchase_order=purchase_order,
                **item_data,
            )

        purchase_order.recalculate_total()
        return purchase_order

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        if instance.status not in [PurchaseOrderStatus.DRAFT, PurchaseOrderStatus.REJECTED]:
            raise serializers.ValidationError(
                "Only draft or rejected purchase orders can be updated."
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if items_data is not None:
            instance.items.all().delete()

            for item_data in items_data:
                PurchaseOrderItem.objects.create(
                    purchase_order=instance,
                    **item_data,
                )

            instance.recalculate_total()

        return instance


class PurchaseOrderStatusSerializer(serializers.Serializer):
    remarks = serializers.CharField(required=False, allow_blank=True)