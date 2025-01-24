from django.contrib import admin
from .views import *  # Import all views from the current module
from .models import *  # Import all models from the current module

# Customize the Django admin interface
admin.site.site_header = "USER"  # Set the header displayed at the top of the admin site

# Register the User_Post model to make it accessible and editable through the Django admin interface
admin.site.register(User_Post)
