"""
ASGI config for DjangoPractise project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import WEBSockets.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoPractise.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http':get_asgi_application(), 
    'websocket': URLRouter(
        WEBSockets.routing.websocket_urlpatterns
    )
})