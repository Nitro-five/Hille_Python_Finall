from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class FavoriteCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_cities')
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city_name} ({self.user.username})"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}...'

    class Meta:
        ordering = ['created_at']
