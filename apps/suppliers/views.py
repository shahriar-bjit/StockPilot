from django.shortcuts import render
from rest_framework import permissions, viewsets
from apps.users.permissions import IsProcurementOfficerOrAdmin
from .models import Supplier
from .serializers import SupplierSerializer

# Create your views here.

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.prefetch_related("products").all()
    serializer_class = SupplierSerializer
    search_fields = ["name", "supplier_code", "email", "contact_person"]
    ordering_fields = ["name", "supplier_code", "created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsProcurementOfficerOrAdmin()]