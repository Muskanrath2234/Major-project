from django.contrib import admin
from .models import Room, Message

# Room model ko admin panel me register kar rahe hain
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id"]  # `first_user` aur `second_user` fields Room model me define hone chahiye

    class Meta:
        model = Room  # Specify the model associated with this admin class

# Message model ko admin panel me register kar rahe hain
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["user", "room", "created_date"]

    class Meta:
        model = Message  # Specify the model associated with this admin class