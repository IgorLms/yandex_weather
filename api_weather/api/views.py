from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from api.services.yandex_api.yandex_weather_api import WeatherYandexApi


class WeatherCity(RetrieveAPIView):
    """Передача данных о погоде с Yandex-API по названию города"""

    def get(self, request, *args, **kwargs):
        if 'city' in self.request.query_params:
            return Response(WeatherYandexApi(self.request.query_params.get('city')).get_request())

        raise ParseError(detail='Нет параметров города')
