from django.contrib import admin
from .models import Ticket

"""
This file registers the Ticket model with the Django admin site,
allowing administrators to manage and interact with tickets from the admin interface.
"""

# Registering the Ticket model with the admin site
admin.site.register(Ticket)