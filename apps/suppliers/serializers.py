from rest_framework import serializers
from apps.inventory.models import Product
from .models import Supplier


class SupplierProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "sku", "unit_price", "stock_on_hand")


class SupplierSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False,
    )
    product_details = SupplierProductSerializer(source="products", many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = (
            "id",
            "name",
            "supplier_code",
            "email",
            "phone",
            "address",
            "contact_person",
            "is_active",
            "products",
            "product_details",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "product_details", "created_at", "updated_at")