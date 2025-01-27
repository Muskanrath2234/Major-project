# Importing necessary modules for WebSocket routing
from django.urls import re_path
from . import consumers

# WebSocket URL patterns for chat application
websocket_urlpatterns = [
    # Handling WebSocket connections for individual chat rooms
    re_path(r"^ws/chat/(?P<room_name>[^/]+)/$", consumers.ChatConsumer.as_asgi()),
]