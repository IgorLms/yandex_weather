# Яндекс погода (API и Телеграм бот)

- Реализовал API, которое на HTTP запрос GET /weather?city=<city_name>, где city_name это название города на русском языке, 
возвращает текущую температуру в этом городе в градусах Цельсия, атмосферное давление (мм.рт.ст.) и скорость ветра (м/с.);
- Реализовал телеграм бота, который после нажатия кнопки "Узнать погоду" при получении названия города будет в ответ присылать прогноз погоды на сегодня;
- Реализовал возможность сохранять данные о погоде в кэше на 30 минут.

## Подготовка окружения

### Redis ([инструкция для Windows](https://redis.io/docs/install/install-redis/install-redis-on-windows/))
```commandline
Откройте PowerShell или командную строку Windows от администратора и введите:
wsl --install
Перезагрузите компьютер это установит дистрибутив Linux Ubuntu.
Создайте пользователя в Ubuntu.

Установите Redis с использованием следующих команд:
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis

Запустите сервер Redis:
sudo service redis-server start

Подключитесь к Redis:
redis-cli 
127.0.0.1:6379> ping
PONG

Таким образом мы получим переменную LOCATION_REDIS, котрая в данном случае равна 127.0.0.1:6379
```

### Yandex API ([инструкция](https://yandex.ru/dev/site/doc/ru/concepts/access))
```commandline
Заходим на сайт доступа к Yandex API и следуя инструкции получаем ключ API.
Переменная X-Yandex-API-Key является этим ключом.
```

### Telegram API ([BotFather](https://telegram.me/BotFather))
```commandline
Перейдите в диалог с инструментом для разработки чатов — https://telegram.me/BotFather.
Нажмите кнопку «Start» или введите в диалоге команду /start.
Далее введите команду /newbot, чтобы сделать новый бот.
Укажите название — как будет отображаться чат в списке контактов.
Последнее — системное имя: это то, что будет ником после знака @.

Таким образом мы получим переменную TELEGRAM_API_TOKEN.
```

### Ngrok ([Ngrok](https://dashboard.ngrok.com/get-started/setup/windows))
```commandline
Скачайте автономный исполняемый файл и введите в нем:
ngrok config add-authtoken 2bGbTTdoIROVkLDpWlAlrGrkGgW_46Y6GcQbZmsfJm3F3fkU5
ngrok http 8000

Таким образом Вы получите ngork_url, например 178c-5-142-84-75.ngrok-free.app.
Важно при каждом перезапуске ngork, ngork_url будет изменён.
Необходимо повторно повторить команду из быстрого старта (python manage.py set_telegram_webhook <ngrok_url>).
```

## Быстрый старт для Windows
```commandline
mkdir название_папки
cd название папки/

git clone https://github.com/IgorLms/yandex_weather.git

cd api_weather/

python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

cd api_weather/

nano .env

LOCATION_REDIS=<LOCATION_REDIS>
X-Yandex-API-Key=<X-Yandex-API-Key>
TELEGRAM_API_TOKEN=<TELEGRAM_API_TOKEN>

python manage.py set_telegram_webhook <ngrok_url>
python manage.py migrate
python manage.py runserver
```