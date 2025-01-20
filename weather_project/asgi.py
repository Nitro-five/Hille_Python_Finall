import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from weather.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')

application = ProtocolTypeRouter({
    """
    Основной ASGI-приложение для маршрутизации запросов.

    Это приложение определяет, как обрабатывать различные типы запросов:
    - HTTP-запросы обрабатываются стандартным ASGI-приложением Django.
    - WebSocket-запросы обрабатываются с помощью AuthMiddlewareStack и URLRouter, которые перенаправляют их на маршруты, определенные в websocket_urlpatterns.

    Параметры:
        - "http": Обрабатывает обычные HTTP-запросы с помощью get_asgi_application().
        - "websocket": Обрабатывает WebSocket-запросы с помощью AuthMiddlewareStack и URLRouter, используя маршруты из websocket_urlpatterns.
    """
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
