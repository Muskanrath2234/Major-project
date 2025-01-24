"""
This file defines the views for managing user profiles within the application.

It includes functionalities to create, update, and display user profiles, 
handling user authentication, and managing personal information such as 
full name, age, contact details, and profile images.

The views use Django's built-in decorators and form handling to ensure 
secure and efficient user interactions with their profiles.
"""
from django.contrib.auth.decorators import login_required  # Import the decorator for login protection
from django.shortcuts import render, redirect  # Import render and redirect for handling HTTP requests and responses
from .models import UserProfile  # Import the UserProfile model

@login_required  # Ensure the user is logged in to access this view
def user_profile(request):
    try:
        profile = request.user.userprofile  # Attempt to retrieve the user's profile using the related_name
    except UserProfile.DoesNotExist:  
        profile = UserProfile.objects.create(user=request.user)  # Create a new profile if it doesn't exist

    if request.method == 'POST':  # Check if the form has been submitted
        profile.full_name = request.POST.get('full_name')  # Update the full name

        # Handle age input properly: if empty, set to None or a default value
        age = request.POST.get('age')
        if age:
            try:
                profile.age = int(age)  # Convert to integer if not empty
            except ValueError:
                profile.age = None  # Set to None if the value is invalid
        else:
            profile.age = None  # Set to None or a default value like 18, if required
        
        profile.room_number = request.POST.get('room_number')  # Update room number
        profile.bed_number = request.POST.get('bed_number')  # Update bed number
        profile.mobile_number = request.POST.get('mobile_number')  # Update mobile number
        profile.aadhar_card = request.POST.get('aadhar_card')  # Update Aadhar card
        profile.pan_card = request.POST.get('pan_card')  # Update PAN card
        profile.bio = request.POST.get('bio')  # Update bio

        # Check if there's a new image uploaded
        if 'image' in request.FILES:
            profile.image = request.FILES['image']  # Update profile image if uploaded

        profile.save()  # Save the updated profile

        # Redirect to avoid resubmitting the form if refreshed
        return redirect('user_profile')  

    return render(request, 'user_profile.html', {'profile': profile})  # Render the profile page

