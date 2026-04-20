from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True) 

    class Meta:
        model = Product
        fields = ("id",
            "category",
            "category_name",
            "name",
            "sku",
            "description",
            "image",
            "unit_price",
            "stock_on_hand",
            "reorder_level",
            "is_active",
            "is_low_stock",
            "created_by",
            "created_by_email",
            "created_at",
            "updated_at",)
        read_only_fields = ("id", "created_at", "updated_at", "is_low_stock", "created_by_email")

    def validate(self, attrs):
        stock_on_hand = attrs.get('stock_on_hand', getattr(self.instance, 'stock_on_hand', 0)) 
        reorder_level = attrs.get('reorder_level', getattr(self.instance, 'reorder_level', 0))

        if stock_on_hand < 0:
            raise serializers.ValidationError({"stock_on_hand": "Stock cannot be negative."})

        if reorder_level < 0:
            raise serializers.ValidationError({"reorder_level": "Reorder level cannot be negative."})

        return attrs