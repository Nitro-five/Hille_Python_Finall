from django.urls import path
from . import consumers

"""
Список маршрутов для WebSocket-соединений.

Каждый путь связывает URL-адрес с соответствующим WebSocket-потребителем.
В данном случае создается маршрут для чата.

Параметры:
    - 'ws/chat/': URL для подключения к чату.
    - consumers.ChatConsumer.as_asgi(): Потребитель, который обрабатывает WebSocket-соединения для чата.
"""
websocket_urlpatterns = [

    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]
