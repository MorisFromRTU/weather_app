import requests
from django.conf import settings

OPENCAGE_API_KEY = settings.OPENCAGE_API_KEY
WEATHER_API_URL = settings.WEATHER_API_URL

def get_coordinates(city):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        return None, None

def get_weather_data(latitude, longitude):
    if latitude is None or longitude is None:
        return None
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
    }
    response = requests.get(WEATHER_API_URL, params=params)
    return response.json()

def get_average_temperatures_by_day(temperatures, timestamps):
    days = []
    current_day = []
    current_date = timestamps[0][:10]
    for i in range(len(temperatures)):
        date = timestamps[i][:10]
        if date == current_date:
            current_day.append((temperatures[i], timestamps[i]))
        else:
            days.append(current_day)
            current_day = [(temperatures[i], timestamps[i])]
            current_date = date
    days.append(current_day)
    average_temperatures_by_day = []
    
    for day_data in days:
        periods = {
            'morning': [], 
            'day': [], 
            'evening': [], 
            'night': []
        }
        for temp, timestamp in day_data:
            hour = int(timestamp[11:13])
            if 6 <= hour < 12:
                periods['morning'].append(temp)
            elif 12 <= hour < 18:
                periods['day'].append(temp)
            elif 18 <= hour < 24:
                periods['evening'].append(temp)
            else:
                periods['night'].append(temp)
        
        average_temperatures = {}
        for period in periods:
            if periods[period]:
                average_temperatures[period] = round(sum(periods[period]) / len(periods[period])), timestamp[:10]
            else:
                average_temperatures[period] = None
        
        average_temperatures_by_day.append(average_temperatures)
    return average_temperatures_by_day
