from django.shortcuts import render
from django.db import models
from rest_framework import filters, permissions, viewsets
from .filters import ProductFilter
from apps.users.permissions import IsInventoryManagerOrAdmin
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'slug']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsInventoryManagerOrAdmin()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'created_by').all() 
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ["name", "sku", "stock_on_hand", "unit_price", "created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsInventoryManagerOrAdmin()] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user) 

    def get_queryset(self):
        queryset = super().get_queryset()
        low_stock = self.request.query_params.get('low_stock')
        
        if low_stock and low_stock.lower() == 'true':
            queryset = queryset.filter(stock_on_hand__lte=models.F('reorder_level'))
        return queryset