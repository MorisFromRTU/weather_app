import requests
from django.shortcuts import render, redirect
from .forms import CityForm, LoginForm, RegistrationForm
from .models import WeatherSearchHistory
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .utils import get_coordinates, get_weather_data, get_average_temperatures_by_day
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import City


def city_autocomplete(request):
    if 'term' in request.GET:
        qs = City.objects.filter(name__icontains=request.GET.get('term'))
        cities = list(qs.values_list('name', flat=True))
        last_search = WeatherSearchHistory.objects.filter(user=request.user).order_by('-timestamp').first()
        cities.insert(0, str(last_search))
        return JsonResponse(cities, safe=False)
        
    return JsonResponse([], safe=False)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User(username=username)
            user.set_password(password)
            user.save()
            return redirect('login') 
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'weather/registration.html', context)

def login_page(request):
    context = {
        'form' : LoginForm()
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            context = {
                'form' : form
            }
    return render(request, 'weather/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')



def index(request):
    weather_data = None
    average_temperatures = []
    error_message = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            coordinates = get_coordinates(city)
            weather_data = get_weather_data(coordinates[0], coordinates[1])
            WeatherSearchHistory.objects.create(user=request.user, city=city)
            if weather_data is None:
                error_message = f"Could not find weather data for city: {city}"
            
            else:
                temperatures = weather_data['hourly']['temperature_2m']
                timestamps = weather_data['hourly']['time']
                average_temperatures = get_average_temperatures_by_day(temperatures, timestamps)
    else:
        form = CityForm()

    context = {
        'form': form,
        'weather_data': weather_data,
        'average_temperatures': average_temperatures,
        'error_message': error_message,
    }

    return render(request, 'weather/index.html', context)
