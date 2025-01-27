import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# File Summary:
# This file defines the models for Room and Message within a Django application, 
# facilitating communication between users through chat rooms and messages.

# Room Model
class Room(models.Model):
    # Unique identifier for each Room using UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ForeignKey to associate the room with the first user
    first_user = models.ForeignKey(User, related_name="room_first", on_delete=models.CASCADE, null=True)
    # ForeignKey to associate the room with the second user
    second_user = models.ForeignKey(User, related_name="room_second", on_delete=models.CASCADE, null=True)

# Message Model
class Message(models.Model):
    # ForeignKey to associate the message with a specific user
    user = models.ForeignKey(User, related_name="messages", verbose_name="User", on_delete=models.CASCADE)
    # ForeignKey to associate the message with a specific room
    room = models.ForeignKey(Room, related_name="messages", verbose_name="Room", on_delete=models.CASCADE)
    # Field to store the content of the message
    content = models.TextField(verbose_name="Message Content")
    # Automatically captures the timestamp when the message is created
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    # Additional field for any other information
    what_is_it = models.CharField(max_length=50, null=True)

    # Method to get the formatted time of message creation
    def get_short_date(self):
        local_time = timezone.localtime(self.created_date)
        return local_time.strftime("%H:%M")

