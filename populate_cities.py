import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')
django.setup()

from weather.models import City

API_URL = "http://api.geonames.org/searchJSON"
USERNAME = "mor1s"

def get_cities():
    params = {
        'q': '',
        'maxRows': 1000,
        'orderby': 'population',
        'username': USERNAME,
        'featureClass': 'P',
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:    
        return response.json()['geonames']
    return []

def populate_cities():
    cities = get_cities()
    for city in cities:
        City.objects.get_or_create(name=city['name'])
if __name__ == '__main__':
    populate_cities()
