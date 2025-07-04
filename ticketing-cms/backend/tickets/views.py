from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from .models import Ticket, TicketComment
from .serializers import (
    TicketSerializer, TicketDetailSerializer, TicketCreateSerializer, 
    TicketUpdateSerializer, TicketCommentSerializer, TicketCommentCreateSerializer
)

# Create your views here.

class TicketListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer
        return TicketSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.all().order_by('-created_at')
        
        if user.is_company_user:
            # Company users can see all tickets for their company's projects
            queryset = queryset.filter(project__company=user.company)
        else:
            # Clients can only see tickets they created or for their projects
            queryset = queryset.filter(
                Q(created_by=user) | Q(project__client=user)
            )
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority_filter = self.request.query_params.get('priority', None)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        # Filter by project
        project_filter = self.request.query_params.get('project', None)
        if project_filter:
            queryset = queryset.filter(project_id=project_filter)
        
        return queryset

class TicketDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TicketUpdateSerializer
        return TicketDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.all()
        
        if user.is_company_user:
            queryset = queryset.filter(project__company=user.company)
        else:
            queryset = queryset.filter(
                Q(created_by=user) | Q(project__client=user)
            )
        
        return queryset

class MyTicketsView(generics.ListAPIView):
    """Get tickets assigned to current user"""
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Ticket.objects.filter(
            assigned_to=self.request.user
        ).order_by('-created_at')

class TicketCommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCommentCreateSerializer
        return TicketCommentSerializer
    
    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        user = self.request.user
        
        # First check if user can access this ticket
        ticket_exists = Ticket.objects.filter(id=ticket_id).exists()
        if not ticket_exists:
            return TicketComment.objects.none()
        
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Check permission to view ticket
        if user.is_company_user:
            can_access = ticket.project.company == user.company
        else:
            can_access = ticket.created_by == user or ticket.project.client == user
        
        if not can_access:
            return TicketComment.objects.none()
        
        # Filter out internal comments for non-company users
        queryset = TicketComment.objects.filter(ticket_id=ticket_id)
        if not user.is_company_user:
            queryset = queryset.filter(is_internal=False)
        
        return queryset.order_by('created_at')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ticket_stats_view(request):
    """Get ticket statistics for current user"""
    user = request.user
    
    if user.is_company_user:
        # Company user stats
        tickets = Ticket.objects.filter(project__company=user.company)
        my_tickets = Ticket.objects.filter(assigned_to=user)
        
        stats = {
            'total_tickets': tickets.count(),
            'open_tickets': tickets.filter(status='open').count(),
            'in_progress_tickets': tickets.filter(status='in_progress').count(),
            'closed_tickets': tickets.filter(status='closed').count(),
            'my_assigned_tickets': my_tickets.count(),
            'my_open_tickets': my_tickets.filter(status__in=['open', 'in_progress']).count(),
            'high_priority_tickets': tickets.filter(priority='high').count(),
            'urgent_tickets': tickets.filter(priority='urgent').count(),
        }
    else:
        # Client user stats
        tickets = Ticket.objects.filter(
            Q(created_by=user) | Q(project__client=user)
        )
        
        stats = {
            'total_tickets': tickets.count(),
            'open_tickets': tickets.filter(status='open').count(),
            'in_progress_tickets': tickets.filter(status='in_progress').count(),
            'closed_tickets': tickets.filter(status='closed').count(),
            'my_created_tickets': tickets.filter(created_by=user).count(),
        }
    
    return Response(stats)
