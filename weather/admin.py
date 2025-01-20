from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели ChatMessage.

    Поля:
        - list_display: Указывает, какие поля модели будут отображаться в списке.
        - search_fields: Определяет поля для поиска.
        - list_filter: Фильтры для отображаемых записей.
        - actions: Определяет список доступных кастомных действий для выбранных записей.
    """
    list_display = ('user', 'message', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('created_at',)
    actions = ['delete_selected_messages']

    @admin.action(description='Удалить выбранные сообщения')
    def delete_selected_messages(self, request, queryset):
        """
        Кастомное действие для удаления выбранных сообщений.

        Параметры:
            request (HttpRequest): Запрос от пользователя.
            queryset (QuerySet): Выбранные записи для удаления.

        После выполнения действия выводится сообщение о количестве удалённых записей.
        """
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Удалено {count} сообщений.")
