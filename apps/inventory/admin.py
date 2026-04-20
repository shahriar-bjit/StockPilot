from django.contrib import admin
from .models import Category, Product, StockMovement

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "unit_price",
        "stock_on_hand",
        "reorder_level",
        "is_active",
        "created_by",
        "created_at",
    )
    list_filter = ("is_active", "category", "created_at")
    search_fields = ("name", "sku")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("category", "created_by")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "movement_type", "quantity", "performed_by", "created_at")
    list_filter = ("movement_type", "created_at")
    search_fields = ("product__name", "product__sku", "reference_note")
    readonly_fields = ("created_at", "updated_at")