from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  # Renamed login to avoid conflict
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room, Message

# View to display all chat rooms
@login_required(login_url='login')  # Redirect to login page if not authenticated
def index(request):
    """
    This view handles the display of all available chat rooms for the logged-in user. 
    It excludes the currently logged-in user from the list of other users.
    """
    # Fetch all users except the currently logged-in user
    users = User.objects.all().exclude(username=request.user.username)
    return render(request, "chat/index.html", {"users": users})

# View to display a specific chat room and messages
@login_required(login_url='login')  # Redirect to login page if not authenticated
def room(request, room_name):
    """
    This view handles the display of a specific chat room and its messages. 
    It includes the list of users, room details, and the ordered messages.
    """
    # Fetch all users except the currently logged-in user
    users = User.objects.all().exclude(username=request.user.username)
    
    # Get the chat room object by its ID
    room = Room.objects.get(id=room_name)
    
    # Get all messages associated with this room, ordered by creation date
    messages = Message.objects.filter(room=room).order_by('created_date')

    return render(request, "chat/room_v2.html", {
        "room_name": room_name,
        "room": room,
        "users": users,
        "messages": messages
    })

# View to start a new chat with a specific user
@login_required(login_url='login')  # Redirect to login page if not authenticated
def start_chat(request, username):
    """
    This view handles the initiation of a new chat with a specific user. 
    If a chat room exists between the two users, it redirects to the room, 
    otherwise, a new chat room is created.
    """
    # Get the second user for the chat
    second_user = User.objects.get(username=username)
    try:
        # Check if a chat room exists between the current user and the second user
        room = Room.objects.get(first_user=request.user, second_user=second_user)
    except Room.DoesNotExist:
        try:
            # If no room exists, check for the reverse pairing
            room = Room.objects.get(second_user=request.user, first_user=second_user)
        except:
            # If neither room exists, create a new chat room
            room = Room.objects.create(first_user=request.user, second_user=second_user)
    return redirect("room", room.id)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .models import Room, Message

# View to delete a chat room
@login_required
def delete_chat(request, room_id):
    """
    This view handles the deletion of a chat room. 
    It checks if the logged-in user is allowed to delete the room 
    and deletes the room if they have the proper permissions.
    """
    # Get the chat room object by its ID
    room = get_object_or_404(Room, id=room_id)

    # Check if the user is either the first_user or second_user
    if request.user != room.first_user and request.user != room.second_user:
        return HttpResponseForbidden("You are not allowed to delete this chat.")

    if request.method == 'GET':
        # Delete the chat room
        room.delete()
        return redirect('index')
    
    return JsonResponse({'status': 'Invalid request'}, status=400)

from django.shortcuts import render, get_object_or_404
from .models import Room
from Admin_Management.models import Profile

# View to display the profile of the second user in a chat room
def second_user_profile_view(request, room_id):
    """
    This view fetches and displays the profile details of the second user in a chat room. 
    It includes user details like username, email, contact number, address, and age.
    """
    # Fetch the room instance
    room = get_object_or_404(Room, id=room_id)
    # Get the second user's profile
    profile = get_object_or_404(Profile, user=room.second_user)
    
    context = {
        'username': profile.user.username,
        'email': profile.email,
        'contact_number': profile.contact_number,
        'address': profile.address,
        'age': profile.age,
        'profile_img_url': profile.profile_img.url,
    }
    
    return render(request, 'chat/second_user_profile_detail.html', context)

