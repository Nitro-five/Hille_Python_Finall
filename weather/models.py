from django.contrib.auth.models import User
from django.db import models


class FavoriteCity(models.Model):
    """
    Модель для сохранения любимых городов пользователя.

    Атрибуты:
        user (ForeignKey): Связь с моделью User, указывающая на пользователя.
        city_name (CharField): Название города.

    Методы:
        __str__: Возвращает строковое представление города и имени пользователя.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_cities')
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city_name} ({self.user.username})"


class SearchStatistic(models.Model):
    """
    Модель для хранения данных о поисковых запросах.

    Атрибуты:
        city_name (CharField): Название города, который искали.
        search_count (IntegerField): Сколько раз город искали.
    """
    city_name = models.CharField(max_length=100, unique=True)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.city_name} ({self.search_count} запросов)"


class ChatMessage(models.Model):
    """
    Модель для хранения сообщений чата.

    Атрибуты:
        user (ForeignKey): Связь с моделью User, указывающая на пользователя, отправившего сообщение.
        message (TextField): Текст сообщения.
        created_at (DateTimeField): Время создания сообщения.

    Методы:
        __str__: Возвращает строковое представление сообщения и имени пользователя.

    Классы:
        Meta: Определяет порядок сортировки сообщений по времени создания.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}...'

    class Meta:
        ordering = ['created_at']
