from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from django.http import JsonResponse, HttpResponseBadRequest

"""
This file contains views for handling support tickets in a Django application. 
It includes functionality for listing, creating, viewing, and updating tickets.
"""

# List tickets
@login_required
def view_all_tickets(request):
    """
    Handles the display of all support tickets.
    Allows users to view a list of tickets ordered by creation date (most recent first).
    If a POST request is made, the associated ticket is deleted.
    """
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.delete()
        
    tickets = Ticket.objects.all().order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})


# Raise a new ticket
@login_required
def raise_ticket(request):
    """
    Handles the creation of a new support ticket.
    If the request method is POST, a form is submitted to create a new ticket associated with the logged-in user.
    If the form is valid, the ticket is saved and the user is redirected to the ticket creation page.
    """
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('raise_ticket')
    else:
        form = TicketForm()
    return render(request, 'support/raise_ticket.html', {'form': form})

# View a ticket detail (for admin)
@login_required
def ticket_detail(request, ticket_id):
    """
    Handles the display of a single ticket's details.
    Allows admin users to view and update the ticket's status.
    If the request method is POST, the ticket's status is updated, and the user is redirected to the ticket detail page.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        ticket.status = status
        ticket.save()
        return redirect('ticket_detail', ticket_id=ticket_id)
    return render(request, 'support/ticket_detail.html', {'ticket': ticket})


