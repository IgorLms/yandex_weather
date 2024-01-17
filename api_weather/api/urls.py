from django.urls import path

from api import views

urlpatterns = [
    path('weather/<str:city>', views.WeatherCity.as_view()),
]
