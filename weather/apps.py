from django.apps import AppConfig


class WeatherConfig(AppConfig):
    """
    Конфигурация приложения "weather".

    Атрибуты:
        default_auto_field (str): Определяет тип автоинкрементного поля для моделей.
        name (str): Имя приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'
