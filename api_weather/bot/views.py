from rest_framework.views import APIView
from telebot import types
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import telebot

from api.services.yandex_api.yandex_weather_api import WeatherYandexApi
from api_weather.settings import bot


class TelegramBot(APIView):

    def post(self, request):
        """Получение сообщений от пользователя в Telegram"""

        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

        return Response({'code': 200})

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start(message):
        """
        Нажатие /start.
        Приветствие в Telegram, создание кнопки "Узнать погоду" и инструкция работы.
        """

        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        weather = types.KeyboardButton('Узнать погоду')
        keyboard_markup.add(weather)
        bot.send_message(
            message.chat.id,
            'Привет! Я погодный бот. Нажми кнопку "Узнать погоду", а далее введи город в котором необходимо узнать погоду.',
            reply_markup=keyboard_markup)

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def btn_weather(message):
        """
        Нажатие кнопки "Узнать погоду".
        Если нажата кнопка "Узнать погоду", то отправляем инструкцию и регистрируем функцию yandex_weather, как следующую к выполнению.
        """

        if message.text == 'Узнать погоду':
            bot.send_message(message.chat.id, 'Напиши мне город в котором необходимо узнать погоду.')
            bot.register_next_step_handler_by_chat_id(message.chat.id, TelegramBot.yandex_weather)
        else:
            bot.send_message(message.chat.id, 'Нажми кнопку "Узнать погоду", а далее введи город в котором необходимо узнать погоду.')

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def yandex_weather(message):
        """
        Ввод города.
        Узнаём погоду в городе и отправляем его в Telegram.
        Регистрируем функцию btn_weather, как следующую к выполнению.
        """

        try:
            # Получаем погоду.
            weather = WeatherYandexApi(message.text).get_request()
            # Отправляем погоду в Telegram.
            bot.send_message(message.chat.id, f'Погода в {message.text}.')
            bot.send_message(message.chat.id, f'Температура {weather['temp']} ℃.')
            bot.send_message(message.chat.id, f'Скорость ветра {weather['wind_speed']} м/с.')
            bot.send_message(message.chat.id, f'Атмосферное давление {weather['pressure_mm']} мм.рт.ст.')
        except NotFound:
            bot.send_message(message.chat.id, 'Данный город не существует. Попробуйте ещё раз.')

        bot.register_next_step_handler_by_chat_id(message.chat.id, TelegramBot.btn_weather)

