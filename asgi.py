import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from core import consumers  # ვქმნით Consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/likes/<int:post_id>/", consumers.LikeConsumer.as_asgi()),
            path("ws/notifications/", consumers.NotificationConsumer.as_asgi()),  # WebSocket URL
        ])
    ),
})
