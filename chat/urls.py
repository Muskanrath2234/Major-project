# Importing necessary modules and views
from django.urls import path
from .views import *

# URL patterns for chat application
urlpatterns = [
    # Home page for chat
    path("", index, name="index"),

    # Individual chat room page
    path("<str:room_name>/", room, name="room"),

    # Start chat with a specific user
    path('start_chat/<str:username>', start_chat, name="start_chat"),

    # Delete a chat room by UUID
    path('room/<uuid:room_id>/delete/', delete_chat, name='delete_chat'),  # Change `int:room_id` to `uuid:room_id`

    # View profile of the second user in a chat
    path('second_user_profile/<uuid:room_id>/', second_user_profile_view, name='second_user_profile_view'),
]

