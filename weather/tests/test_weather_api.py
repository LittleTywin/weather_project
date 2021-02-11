from django.test import SimpleTestCase

from django.conf import settings
from weather.weather_api import WeatherApi

class TestWeatherApi(SimpleTestCase):

    def setUp(self):
        self.weather_api = WeatherApi(settings.WEATHER_API_KEY)
        self.key_subset = set(['coord','weather','main','dt','id','name'])

    def test_current_weather_by_id(self):
        response = self.weather_api.current(id=2172797)
        data = response.json()
        self.assertEqual(data['cod'], 200)
        self.assertTrue(self.key_subset.issubset(data.keys()))
    
    def test_current_weather_by_lon_lat(self):
        response = self.weather_api.current(lon=22, lat=31)
        data = response.json()
        self.assertEqual(data['cod'], 200)
        self.assertTrue(self.key_subset.issubset(data.keys()))
    
    def test_current_weather_location_circle(self):
        response = self.weather_api.find(lon=22.075851, lat=39.256406, count=10)
        data = response.json()
        self.assertEqual(data['cod'], '200')
        self.assertEqual(len(data['list']),10)
        