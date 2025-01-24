from django.urls import path
from .views import *  # Import all views from the current module

# URL patterns to map URLs to views
urlpatterns = [
    # Landing page URL pattern
    path('', landing, name='landing'),  # Maps the root URL ('') to the 'landing' view

    # About page URL pattern
    path('about/', about, name='about'),  # Maps the '/about/' URL to the 'about' view

    # Contact form submission URL pattern
    path('contact/', contact_view, name='contact'),  # Maps '/contact/' URL to the 'contact_view' view

    # Service page URL pattern
    path('service/', service, name='service'),  # Maps '/service/' URL to the 'service' view

    # Subscription URL pattern
    path('subscribe/', subscribe, name='subscribe'),  # Maps '/subscribe/' URL to the 'subscribe' view

    # Base login URL pattern
    path('base_login/', base_login, name='base_login'),  # Maps '/base_login/' URL to the 'base_login' view
]
