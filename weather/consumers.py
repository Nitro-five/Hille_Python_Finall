import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket-потребитель для чата, использующий Django Channels.

    Методы:
        connect: Подключает пользователя к группе сообщений.
        disconnect: Отключает пользователя от группы сообщений.
        receive: Обрабатывает входящие сообщения от клиента.
        chat_message: Отправляет сообщение клиенту после получения из группы.
    """

    async def connect(self):
        """
        Обрабатывает установление WebSocket-соединения.

        Подключает пользователя к группе сообщений на основе имени комнаты.
        """
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Обрабатывает отключение WebSocket-соединения.

        Отключает пользователя от группы сообщений.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Обрабатывает получение сообщения от клиента WebSocket.

        Десериализует сообщение и отправляет его в группу.

        Параметры:
            text_data (str): Сообщение в формате JSON, полученное от клиента.
        """
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        """
        Отправляет сообщение обратно клиенту WebSocket.

        Получает сообщение из группы и отправляет его обратно на WebSocket.

        Параметры:
            event (dict): Сообщение из группы, содержащие данные 'message' и 'username'.
        """
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
