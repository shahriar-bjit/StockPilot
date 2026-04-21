from django.contrib import admin
from .models import Supplier

# Register your models here.

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier_code', 'email', 'phone', 'contact_person', 'is_active', 'created_at')
    search_fields = ('name', 'supplier_code', 'email', 'contact_person')
    list_filter = ('is_active', "created_at")
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('products',)