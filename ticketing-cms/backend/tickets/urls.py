from django.urls import path
from . import views

urlpatterns = [
    # Tickets
    path('', views.TicketListCreateView.as_view(), name='ticket-list-create'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('my-tickets/', views.MyTicketsView.as_view(), name='my-tickets'),
    path('stats/', views.ticket_stats_view, name='ticket-stats'),
    
    # Ticket Comments
    path('<int:ticket_id>/comments/', views.TicketCommentListCreateView.as_view(), name='ticket-comments'),
]