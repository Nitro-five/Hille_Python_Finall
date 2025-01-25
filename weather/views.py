from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
import requests
from django.conf import settings
from django.contrib import messages
from .models import FavoriteCity, ChatMessage, SearchStatistic


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


def index_view(request):
    """
    Отображает главную страницу сайта.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает главную страницу.
    """
    return render(request, 'weather/index.html')


@login_required
def favorite_cities_view(request):
    """
    Отображает список избранных городов пользователя.

    Проверяет, авторизован ли пользователь, и если да, отображает его избранные города.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает страницу с избранными городами.
    """
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    favorite_cities = user.favorite_cities.all()

    context = {
        'favorite_cities': favorite_cities,
    }
    return render(request, 'weather/favorites.html', context)


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
                search_stat, created = SearchStatistic.objects.get_or_create(city_name=city)
                search_stat.search_count += 1
                search_stat.save()

                return render(request, 'weather/index.html', {
                    'weather': weather_data,  # Передаём погоду в шаблон
                    'city': city
                })
            except requests.RequestException as e:
                error = f"Ошибка запроса к API: {e}"

    return render(request, 'weather/index.html', {'weather': weather_data, 'error': error})


@login_required
def statistics_view(request):
    # Получаем 5 самых популярных городов
    popular_cities = SearchStatistic.objects.order_by('-search_count')[:5]

    # Получаем количество активных пользователей (например, заходили за последние 24 часа)
    from django.utils.timezone import now, timedelta
    active_users_count = User.objects.filter(last_login__gte=now() - timedelta(days=1)).count()

    context = {
        'popular_cities': popular_cities,
        'active_users_count': active_users_count,
    }
    return render(request, 'weather/statistics.html', context)


@login_required
def forecast_view(request):
    """
    Отображает прогноз погоды на несколько дней.

    В зависимости от параметра 'period' отображает прогноз на завтра или на неделю.

    Параметры:
        request (HttpRequest): Запрос пользователя.

    Возвращает:
        HttpResponse: Отображает прогноз погоды на выбранный период.
    """
    city = request.GET.get('city')
    period = request.GET.get('period', 'tomorrow')

    try:
        url = f"http://api.weatherapi.com/v1/forecast.json"
        params = {
            "key": settings.WEATHER_API_KEY,
            "q": city,
            "days": 7,
            "lang": "ru",
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if period == 'tomorrow':
            forecast = data['forecast']['forecastday'][1]  # Прогноз на завтра
        elif period == 'week':
            forecast = data['forecast']['forecastday']  # Прогноз на неделю
        else:
            forecast = None

        context = {
            'city': city,
            'forecast': forecast,
            'period': period,
        }
    except (requests.RequestException, KeyError) as e:
        context = {
            'city': city,
            'error': 'Не удалось получить данные о погоде. Пожалуйста, попробуйте снова.',
        }

    return render(request, 'weather/forecast.html', context)


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
