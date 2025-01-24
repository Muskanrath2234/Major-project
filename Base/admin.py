# Importing required modules from Django
from django.contrib import admin  # To register models with Django admin
from .views import *  # Importing views (though not typically needed here)
from .models import *  # Importing models to register them with the admin interface

# Customizing the site header of the admin interface
admin.site.site_header = "USER"  # Changes the header text on the Django admin panel

# Registering the Subscription model with the admin interface
admin.site.register(Subscription)  # Allows managing Subscription objects via the Django admin

# Customizing the admin view for the ContactSubmission model
@admin.register(ContactSubmission)  # Registering the ContactSubmission model with custom admin settings
class ContactSubmissionAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('id', 'name', 'email', 'subject', 'submitted_at')  # The fields displayed in the table view
    # Enabling search functionality for the specified fields
    search_fields = ('name', 'email', 'subject')  # Allows searching through these fields in the admin interface
    # Adding filter options for the 'submitted_at' field
    list_filter = ('submitted_at',)  # Filter submissions by submission date
