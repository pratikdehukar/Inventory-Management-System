from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'client', 'project_manager', 'status', 'start_date', 'end_date', 'is_active']
    list_filter = ['status', 'company', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'company__name', 'client__username']
    readonly_fields = ['created_at', 'updated_at', 'total_tickets', 'open_tickets', 'closed_tickets']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'company')
        }),
        ('Project Team', {
            'fields': ('client', 'project_manager')
        }),
        ('Project Details', {
            'fields': ('status', 'start_date', 'end_date', 'budget', 'is_active')
        }),
        ('Statistics', {
            'fields': ('total_tickets', 'open_tickets', 'closed_tickets'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
