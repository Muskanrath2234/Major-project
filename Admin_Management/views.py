from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.conf import settings

import random
from django.contrib.auth.models import User
from django.shortcuts import redirect

@csrf_exempt
def verifyOPT(request):
    # OTP verification logic
    if request.method == 'POST':
        useropt = request.POST.get('otp')
        original_otp = request.POST.get('original_otp')  # OTP sent via email
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verify OTP and passwords
        if useropt == original_otp:
            if password1 == password2:
                # Create the user if OTP is valid and passwords match
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                # Return success response
                return JsonResponse({'success': True})
            else:
                # Passwords do not match
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
        else:
            # Invalid OTP
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

    # Return an error if request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def home(request):
    # Render the home page
    return render(request, 'home.html')

def budget(request):
    # Render the budget page
    return render(request, 'budget.html')

def register_user(request):
    # User registration logic
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            otp = random.randint(100000, 999999)

            # Send OTP to the user's email
            messages.success(request, 'Registration successful! Please verify your email.')
            send_mail(
                "User Data",
                f"Verify your email using the OTP: \n {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=True
            )

            # Render the verify page with the OTP and user details for verification
            return render(request, 'verify.html', context={
                'otp': otp,
                'username': username,
                'email': email,
                'password1': password1,
                'password2': password2
            })

            # The form.save() and redirect won't be executed because the return statement is above

        else:
            # Show error if form is not valid
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'register.html', {'form': form})

    else:
        form = CreateUserForm()

    return render(request, 'register.html', {'form': form})

def view_all_users(request):
    # Fetch and display all users
    users = User.objects.all()
    return render(request, 'view_all_users.html', {'users': users})

def user_logout(request):
    # Log out the user and redirect to admin login page
    logout(request)
    return redirect('admin_login')

@login_required
def view_profile(request):
    # Render the profile page for the logged-in user
    user = request.user
    return render(request, 'view_profile.html', {'user': user})

@login_required(login_url='admin_login')
def editprofile(request):
    # Allow the user to edit their profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, Your profile is updated.')
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {'form': form}
    return render(request, 'editprofile.html', context)

def user_logout(request):
    # Another logout function that redirects to base login page
    logout(request)
    return redirect('base_login')

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def change_password(request):
    # Password change logic for the logged-in user
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check if current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, 'The current password is incorrect.')
            return redirect('change_password')

        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'The new passwords do not match.')
            return redirect('change_password')

        # Check if new password meets the minimum length
        if len(new_password) < 8:
            messages.error(request, 'The new password must be at least 8 characters long.')
            return redirect('change_password')

        # Update the password
        request.user.set_password(new_password)
        request.user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password has been successfully updated.')
        return redirect('change_password')

    # Render the change password page
    return render(request, 'change_password.html')


def example_view(request):
    breadcrumb_data = [
        ('Home', 'home'),
        ('User', 'user'),
        ('Add User', 'add_user'),
    ]
    return render(request, 'example_template.html', {'breadcrumb': breadcrumb_data})
