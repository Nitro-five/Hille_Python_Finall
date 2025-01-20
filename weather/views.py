from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
import requests
from django.conf import settings
from django.contrib import messages
from .models import FavoriteCity, ChatMessage


def register_view(request):
    """
    Обрабатывает регистрацию нового пользователя.

    При POST-запросе создает нового пользователя, а затем сразу авторизует его.
    При успешной регистрации выполняется редирект на страницу погоды.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает форму регистрации.
    """
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
    """
    Обрабатывает процесс авторизации пользователя.

    При POST-запросе проверяет имя пользователя и пароль. Если они правильные,
    то авторизует пользователя и перенаправляет на страницу погоды.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает форму авторизации или редирект на страницу погоды.
    """
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
    """
    Обрабатывает выход пользователя из системы.

    Осуществляет выход из системы и редиректит на страницу авторизации.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Редирект на страницу авторизации.
    """
    logout(request)
    return redirect('login')


@login_required
def favorite_cities_view(request):
    """
    Отображает список любимых городов пользователя.

    Доступно только авторизованным пользователям.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает список избранных городов.
    """
    favorites = request.user.favorite_cities.all()
    return render(request, 'weather/favorites.html', {'favorites': favorites})


@login_required
def add_favorite_city(request):
    """
    Добавляет новый город в список избранных для авторизованного пользователя.

    При POST-запросе проверяет, существует ли уже такой город в списке избранных.
    Если нет — добавляет его.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        JsonResponse: Ответ с результатом добавления города.
    """
    if request.method == "POST":
        city_name = request.POST.get('city_name', '').strip()

        if city_name:
            # Попробуем добавить в избранное, если такого города еще нет
            favorite_city, created = FavoriteCity.objects.get_or_create(user=request.user, city_name=city_name)

            if created:
                messages.success(request, f'{city_name} добавлен в избранное.')
            else:
                messages.info(request, f'{city_name} уже в избранном.')

            return redirect('weather')  # Перенаправление на страницу погоды

        messages.error(request, 'Некорректное имя города.')

    return redirect('weather')

@login_required
def remove_favorite_city(request, city_id):
    """
    Удаляет город из списка избранных пользователя.

    Параметры:
        request (HttpRequest): Запрос пользователя.
        city_id (int): ID города для удаления из избранного.

    Возвращает:
        HttpResponse: Редирект на страницу с избранными городами.
    """
    city = get_object_or_404(FavoriteCity, id=city_id, user=request.user)
    city.delete()
    return redirect('favorite_cities')


@login_required
def weather_view(request):
    """
    Отображает страницу погоды для указанного города.

    При POST-запросе извлекает данные о погоде через API и отображает их пользователю.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает данные о погоде или сообщение об ошибке.
    """
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
    """
    Отображает и обрабатывает сообщения чата.

    При POST-запросе сохраняет новое сообщение и отображает все сообщения чата.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает чат с сообщениями.
    """
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Сохраняем сообщение в базе данных
            ChatMessage.objects.create(user=request.user, message=message)

    # Получаем все сообщения
    messages = ChatMessage.objects.all()
    return render(request, 'weather/chat.html', {'messages': messages})
