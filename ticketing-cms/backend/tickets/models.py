from django.db import models
from django.conf import settings

class Ticket(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )

    CATEGORY_CHOICES = (
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('support', 'Support'),
        ('question', 'Question'),
        ('improvement', 'Improvement'),
    )

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Relationships
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tickets')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='assigned_tickets')
    
    # Ticket properties
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='support')
    
    # File attachments
    attachment = models.FileField(upload_to='ticket_attachments/', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket_id} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            # Generate ticket ID
            last_ticket = Ticket.objects.filter(
                project=self.project
            ).order_by('-id').first()
            
            if last_ticket:
                last_number = int(last_ticket.ticket_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.ticket_id = f"{self.project.company.name[:3].upper()}-{self.project.id}-{new_number:04d}"
        
        super().save(*args, **kwargs)

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    attachment = models.FileField(upload_to='comment_attachments/', blank=True)
    is_internal = models.BooleanField(default=False)  # For internal company notes
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment on {self.ticket.ticket_id} by {self.user.username}"
