from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Product(models.Model):
    """Model representing a product in the manufacturing system"""
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    description = models.TextField(blank=True)
    unit_of_measure = models.CharField(max_length=20, default='pieces')
    standard_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"


class ProductionLine(models.Model):
    """Model representing a production line in the manufacturing facility"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity_per_hour = models.PositiveIntegerField(help_text="Units per hour")
    is_active = models.BooleanField(default=True)
    maintenance_schedule = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def current_status(self):
        """Return current status of the production line"""
        if not self.is_active:
            return 'Inactive'
        
        # Check if there are any active work orders
        active_orders = self.workorder_set.filter(status='in_progress').count()
        if active_orders > 0:
            return 'Running'
        
        # Check if maintenance is due
        if self.maintenance_schedule and self.maintenance_schedule <= timezone.now():
            return 'Maintenance Due'
        
        return 'Available'


class WorkOrder(models.Model):
    """Model representing a work order for production"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Normal'),
        (3, 'High'),
        (4, 'Urgent'),
        (5, 'Critical'),
    ]

    work_order_id = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    
    # Scheduling
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    
    # Quantities
    quantity_completed = models.PositiveIntegerField(default=0)
    quantity_scrapped = models.PositiveIntegerField(default=0)
    
    # Personnel
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_work_orders')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_work_orders')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    notes = models.TextField(blank=True)
    estimated_duration = models.DurationField(null=True, blank=True)

    class Meta:
        ordering = ['-priority', 'scheduled_start']

    def __str__(self):
        return f"{self.work_order_id} - {self.product.name}"

    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.status == 'completed':
            return 100
        elif self.status == 'in_progress':
            if self.actual_start and self.scheduled_end:
                total_time = (self.scheduled_end - self.scheduled_start).total_seconds()
                elapsed_time = (timezone.now() - self.actual_start).total_seconds()
                progress = min(int((elapsed_time / total_time) * 100), 95) if total_time > 0 else 0
                return progress
        return 0

    @property
    def completion_rate(self):
        """Calculate completion rate based on quantity"""
        if self.quantity > 0:
            return round((self.quantity_completed / self.quantity) * 100, 2)
        return 0

    def can_start(self):
        """Check if work order can be started"""
        return self.status in ['pending', 'draft'] and self.production_line and self.production_line.is_active

    def start_production(self, user=None):
        """Start production for this work order"""
        if self.can_start():
            self.status = 'in_progress'
            self.actual_start = timezone.now()
            if user:
                self.assigned_to = user
            self.save()
            return True
        return False

    def complete_production(self):
        """Complete production for this work order"""
        if self.status == 'in_progress':
            self.status = 'completed'
            self.actual_end = timezone.now()
            if self.quantity_completed == 0:
                self.quantity_completed = self.quantity
            self.save()
            return True
        return False
