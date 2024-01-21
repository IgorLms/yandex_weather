from django.urls import path

from api import views

urlpatterns = [
    path('weather', views.WeatherCity.as_view(), name="weather_api")
]
