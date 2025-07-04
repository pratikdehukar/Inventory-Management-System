from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from production.models import Product


class Warehouse(models.Model):
    """Model representing a warehouse location"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(help_text="Maximum storage capacity")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Inventory(models.Model):
    """Model representing inventory levels for products"""
    STOCK_TYPE_CHOICES = [
        ('raw', 'Raw Material'),
        ('wip', 'Work in Progress'),
        ('finished', 'Finished Goods'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    stock_type = models.CharField(max_length=20, choices=STOCK_TYPE_CHOICES)
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    reorder_point = models.PositiveIntegerField(default=0)
    max_stock_level = models.PositiveIntegerField(default=1000)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'warehouse', 'stock_type']
        ordering = ['product__name', 'warehouse__name']

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name} ({self.stock_type})"

    @property
    def available_quantity(self):
        """Calculate available quantity (total - reserved)"""
        return max(0, self.quantity - self.reserved_quantity)

    @property
    def needs_reorder(self):
        """Check if stock level is below reorder point"""
        return self.available_quantity <= self.reorder_point


class StockMovement(models.Model):
    """Model for tracking stock movements"""
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
    ]
    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField(validators=[MinValueValidator(-999999)])
    reference_number = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.movement_type} - {self.inventory.product.name} ({self.quantity})"