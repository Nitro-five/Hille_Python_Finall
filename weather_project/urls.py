from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from weather import views

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
urlpatterns = [
    path('remove-favorite/<int:city_id>/', views.remove_favorite_city, name='remove_favorite'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.weather_view, name='weather'),
    path('favorites/', views.favorite_cities_view, name='favorite_cities'),
    path('add-favorite/', views.add_favorite_city, name='add_favorite'),
    path('chat/', views.chat_view, name='chat'),
]
