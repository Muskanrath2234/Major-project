from django.urls import path
from .views import *

urlpatterns = [
    # Home page route, it renders the home page view
    path('', home, name='home'),

    # Register page route, it handles user registration and displays the registration form
    path('register/', register_user, name='register'),

    # View all users route, it displays a list of all users
    path('view_all_user/', view_all_users, name='view_all_users'),

    # Profile page route, it displays the logged-in user's profile details
    path('view_profile/', view_profile, name='view_profile'),

    # Edit profile page route, it allows the user to edit their profile details
    path('editprofile/', editprofile, name='editprofile'),

    # User logout route, it logs the user out and redirects them to the login page
    path('user_logout/', user_logout, name='user_logout'),

    # OTP verification route, it verifies the OTP for user registration or login
    path('verifyEmail', verifyOPT, name='verifyEmail'),

    # Budget page route, it renders the budget page for the user
    path('budget/', budget, name='budget'),

    
]
