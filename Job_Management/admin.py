from django.contrib import admin
from .models import *

# Register your models here.

# Registering Room and Booking models to make them manageable via the Django admin interface
admin.site.register(Job)
admin.site.register(JobApplication)

