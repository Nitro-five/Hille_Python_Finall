from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
import requests
from django.conf import settings
from django.http import JsonResponse
from .models import FavoriteCity, ChatMessage


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            return redirect('weather')  # Перенаправление на страницу погоды
    else:
        form = UserRegistrationForm()
    return render(request, 'weather/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('weather')  # Перенаправление на страницу погоды
        else:
            return render(request, 'weather/login.html', {'error': 'Неправильное имя пользователя или пароль'})
    return render(request, 'weather/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def favorite_cities_view(request):
    favorites = request.user.favorite_cities.all()
    return render(request, 'weather/favorites.html', {'favorites': favorites})


@login_required
def add_favorite_city(request):
    if request.method == "POST":
        city_name = request.POST.get('city_name', '').strip()
        print(f"Received city_name: {city_name}")
        print(f"Request POST data: {request.POST}")

        if city_name:
            # Попробуем добавить в избранное, если такого города еще нет
            favorite_city, created = FavoriteCity.objects.get_or_create(user=request.user, city_name=city_name)

            # Выведем информацию о том, добавился ли город или он уже был
            print(f"City created: {created}, Favorite city: {favorite_city.city_name}")

            if created:
                message = f'{city_name} добавлен в избранное.'
            else:
                message = f'{city_name} уже в избранном.'

            return render(request, 'weather/index.html', {'weather': request.session.get('weather_data'),
                                                          'message': f'{city_name} добавлен в избранное.'})

        return JsonResponse({'status': 'error', 'message': 'Некорректное имя города.'})

    return JsonResponse({'status': 'error', 'message': 'Некорректный метод запроса.'})


@login_required
def remove_favorite_city(request, city_id):
    city = get_object_or_404(FavoriteCity, id=city_id, user=request.user)
    city.delete()
    return redirect('favorite_cities')


@login_required  # Ограничиваем доступ к странице погоды только для авторизованных пользователей
def weather_view(request):
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            url = "http://api.weatherapi.com/v1/current.json"
            params = {
                "key": settings.WEATHER_API_KEY,
                "q": city,
                "aqi": "no"
            }
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                weather_data = response.json()
            except requests.RequestException as e:
                error = f"Ошибка запроса к API: {e}"

    return render(request, 'weather/index.html', {'weather': weather_data, 'error': error})


@login_required
def chat_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Сохраняем сообщение в базе данных
            ChatMessage.objects.create(user=request.user, message=message)

    # Получаем все сообщения
    messages = ChatMessage.objects.all()
    return render(request, 'weather/chat.html', {'messages': messages})
