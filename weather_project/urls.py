from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from weather import views

# Создаем представление для отображения схемы API
schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version='v1',
        description="Документация  API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
"""
Список маршрутов URL для приложения.

Каждый маршрут обрабатывает различные запросы:
- Путь 'remove-favorite/<int:city_id>/' удаляет город из списка избранных.
- Путь 'swagger' отображает документацию API в формате Swagger.
- Путь 'redoc' отображает документацию API в формате ReDoc.
- Путь 'register' и 'login' обрабатывают страницы регистрации и авторизации пользователя.
- Путь 'favorites' и 'add-favorite' обрабатывают действия с избранными городами.
- Путь 'chat' обрабатывает сообщения чата.

Пример документации API доступен по маршруту 'swagger/' и 'redoc/'.
"""
urlpatterns = [
    path('remove-favorite/<int:city_id>/', views.remove_favorite_city, name='remove_favorite'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.weather_view, name='weather'),  # Главная страница
    path('favorites/', views.favorite_cities_view, name='favorite_cities'),
    path('forecast/', views.forecast_view, name='forecast'),
    path('add-favorite/', views.add_favorite_city, name='add_favorite'),
    path('chat/', views.chat_view, name='chat'),
    path('index/', views.index_view, name='home'),
]

