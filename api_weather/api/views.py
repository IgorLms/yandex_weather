from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from api.services.yandex_api.yandex_weather_api import WeatherYandexApi


class WeatherCity(RetrieveAPIView):
    """Передача данных о погоде с Yandex-API по названию города"""

    def get(self, request, *args, **kwargs):
        return Response(WeatherYandexApi(kwargs['city']).get_request())
