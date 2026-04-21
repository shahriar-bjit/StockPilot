from django.db import models
from apps.inventory.models import Product 

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Supplier(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    supplier_code = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True, related_name='suppliers')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['supplier_code']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.supplier_code})" 