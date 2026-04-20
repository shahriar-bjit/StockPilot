from django.db import models
import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="unit_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="unit_price", lookup_expr="lte")
    low_stock = django_filters.BooleanFilter(method="filter_low_stock")

    class Meta:
        model = Product
        fields = ["category", "is_active", "created_by"]

    def filter_low_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_on_hand__lte=models.F("reorder_level"))
        return queryset