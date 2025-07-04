from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE, related_name='projects')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='client_projects', limit_choices_to={'user_type': 'client'})
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                       null=True, blank=True, related_name='managed_projects',
                                       limit_choices_to={'user_type__in': ['company_admin', 'company_staff']})
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.company.name}"

    @property
    def total_tickets(self):
        return self.tickets.count()

    @property
    def open_tickets(self):
        return self.tickets.filter(status__in=['open', 'in_progress']).count()

    @property
    def closed_tickets(self):
        return self.tickets.filter(status='closed').count()
