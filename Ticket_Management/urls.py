from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for viewing all tickets
    path('tickets/', views.view_all_tickets, name='ticket_list'),

    # URL pattern for raising a new ticket
    path('raise-ticket/', views.raise_ticket, name='raise_ticket'),

    # URL pattern for viewing ticket details by ticket ID
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]