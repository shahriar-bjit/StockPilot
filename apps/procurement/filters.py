import django_filters

from .models import PurchaseOrder

class PurchaseOrderFilter(django_filters.FilterSet):
    min_total = django_filters.NumberFilter(field_name="total_amount", lookup_expr="gte")
    max_total = django_filters.NumberFilter(field_name="total_amount", lookup_expr="lte")
    order_date_from = django_filters.DateFilter(field_name="order_date", lookup_expr="gte")
    order_date_to = django_filters.DateFilter(field_name="order_date", lookup_expr="lte")

    class Meta:
        model = PurchaseOrder
        fields = [
            "supplier",
            "status",
            "created_by",
            "approved_by",
        ]