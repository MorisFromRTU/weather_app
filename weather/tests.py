from django.test import TestCase
from .forms import CityForm
from django.urls import reverse

class CityFormTest(TestCase):
    def test_city_form_valid(self):
        form = CityForm(data={'city': 'New York'})
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        form = CityForm(data={'city': ''})
        self.assertFalse(form.is_valid())

class WeatherViewTest(TestCase):
    def test_weather_view_get(self):
        response = self.client.get(reverse('weather'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weather App")

    def test_weather_view_post(self):
        response = self.client.post(reverse('weather'), data={'city': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weather in New York")
