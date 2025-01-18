from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')  # Отображаемые поля в списке
    search_fields = ('user__username', 'message')  # Поля для поиска
    list_filter = ('created_at',)  # Фильтры по дате
    actions = ['delete_selected_messages']  # Добавляем кастомное действие

    @admin.action(description='Удалить выбранные сообщения')
    def delete_selected_messages(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Удалено {count} сообщений.")

