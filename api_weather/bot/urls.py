from django.urls import path

from .views import TelegramBot

urlpatterns = [
    path('', TelegramBot.as_view(), name='weather_telegram'),
]
