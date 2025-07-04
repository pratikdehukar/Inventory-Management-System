from django.contrib import admin
from .models import Ticket, TicketComment

class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'title', 'project', 'created_by', 'assigned_to', 'priority', 'status', 'category', 'created_at']
    list_filter = ['status', 'priority', 'category', 'project__company', 'created_at']
    search_fields = ['ticket_id', 'title', 'description', 'created_by__username']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']
    inlines = [TicketCommentInline]
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('ticket_id', 'title', 'description', 'project')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Properties', {
            'fields': ('priority', 'status', 'category', 'attachment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at', 'closed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'comment_preview', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at', 'ticket__project__company']
    search_fields = ['comment', 'ticket__ticket_id', 'user__username']
    readonly_fields = ['created_at']
    
    def comment_preview(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = "Comment Preview"
