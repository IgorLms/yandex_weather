import os
import requests
import pandas as pd
from rest_framework.exceptions import NotFound
from rest_framework import status

from api_weather.settings import BASE_DIR


class SearchCity(object):
    """Поиск координат по названию города в csv файле"""

    def __init__(self, city: str):
        self.city = city  # Название города
        self.lat, self.lon = self.__validate_coord_city()  # Широта, долгота

    def __get_coord_city(self):
        """Поиск координат по названию города в csv файле"""

        city_csv = pd.read_csv(f'{BASE_DIR}/data/city.csv')
        search_city_line = city_csv.query(f"city == '{self.city.title()}'")
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
        self.headers = {'X-Yandex-API-Key': os.environ.get('X-Yandex-API-Key')}  # Значение ключа Yandex-API
        self.payload = {'lat': self.lat, 'lon': self.lon, 'lang': self.lang, 'limit': self.limit, 'hours': self.hours, 'extra': self.extra}  # Список параметров

    def get_request(self):
        """Получение данных о погоде с Yandex-API"""

        request = requests.get(self.urls, params=self.payload, headers=self.headers)
        request_json = request.json()

        temp = request_json['fact']['temp']  # Температура
        wind_speed = request_json['fact']['wind_speed']  # Скорость ветра
        pressure_mm = request_json['fact']['pressure_mm']  # Давление

        return {'temp': temp, 'wind_speed': wind_speed, 'pressure_mm': pressure_mm}
