import requests
import pandas as pd
from django.conf import settings
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.core.cache import cache

from api_weather.settings import BASE_DIR, CACHE_TTL


class SearchCity(object):
    """Поиск координат по названию города в csv файле"""

    def __init__(self, city: str):
        self.city = city.title()  # Название города
        self.lat, self.lon = self.__validate_coord_city()  # Широта, долгота

    def __get_coord_city(self):
        """Поиск координат по названию города в csv файле"""

        city_csv = pd.read_csv(f'{BASE_DIR}/data/city.csv')
        search_city_line = city_csv.query(f"city == '{self.city}'")
        return search_city_line.get('geo_lat').values, search_city_line.get('geo_lon').values

    def __validate_coord_city(self):
        """Валидация полученных координат"""

        lat, lon = self.__get_coord_city()

        if not len(lat) or not len(lon):
            raise NotFound(detail='Данный город не существует', code=status.HTTP_404_NOT_FOUND)

        return lat[0], lon[0]


class WeatherYandexApi(SearchCity):
    """Получение данных о погоде с Yandex-API по координатам города"""

    def __init__(self, city: str):
        super().__init__(city)
        self.urls = 'https://api.weather.yandex.ru/v2/forecast'  # Url Yandex-API
        self.lang = 'ru_RU'  # Язык ответа
        self.limit = '1'  # Срок прогноза
        self.hours = 'false'  # Наличие почасового прогноза
        self.extra = 'false'  # Подробный прогноз осадков
        self.headers = {'X-Yandex-API-Key': settings.YANDEX_API_KEY}  # Значение ключа Yandex-API
        self.payload = {'lat': self.lat, 'lon': self.lon, 'lang': self.lang, 'limit': self.limit, 'hours': self.hours, 'extra': self.extra}  # Список параметров

    # @method_decorator(cache_page(60 * 30))  # 30 минут кэширования запроса
    def get_request(self):
        """Получение данных о погоде с Yandex-API"""

        if self.city in cache:
            # Получаем погоду из кэша.
            request_json = cache.get(self.city)
        else:
            # Получаем погоду из Яндекс.
            request = requests.get(self.urls, params=self.payload, headers=self.headers)
            request_json = request.json()
            # Заполняем данные в кэш.
            cache.set(self.city, request_json, timeout=CACHE_TTL)

        temp = request_json['fact']['temp']  # Температура
        wind_speed = request_json['fact']['wind_speed']  # Скорость ветра
        pressure_mm = request_json['fact']['pressure_mm']  # Давление

        return {'temp': temp, 'wind_speed': wind_speed, 'pressure_mm': pressure_mm}
