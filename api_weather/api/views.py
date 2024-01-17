from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from api.services.yandex_api.yandex_weather_api import WeatherYandexApi


class WeatherCity(RetrieveAPIView):
    """Передача данных о погоде с Yandex-API по названию города"""

    @method_decorator(cache_page(60 * 30))  # 30 минут кэширования запроса
    def get(self, request, *args, **kwargs):
        return Response(WeatherYandexApi(kwargs['city']).get_request())
