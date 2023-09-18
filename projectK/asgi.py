"""
ASGI config for projectX project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from django.urls import path

from personal.consumers import PersonalChatConsumer,OnlineStatusConsumer

from channels.routing import ProtocolTypeRouter,URLRouter

from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectX.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket':AuthMiddlewareStack(
        URLRouter([
          path('ws/<int:id>/',PersonalChatConsumer.as_asgi()),
          path('ws/online/',OnlineStatusConsumer.as_asgi()),
          
                   
        ])
    )
})
