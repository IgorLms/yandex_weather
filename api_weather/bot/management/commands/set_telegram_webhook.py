import requests

from django.conf import settings
from django.core.management import BaseCommand
from django.urls import reverse


class Command(BaseCommand):
    """Команда для установки нового webhook url для Telegram"""

    def add_arguments(self, parser):
        parser.add_argument("webhook", type=str)

    def handle(self, *args, **options):
        root_url = options["webhook"]
        webhook_path = reverse("weather_telegram")
        webhook_url = f"{root_url}{webhook_path}"
        set_webhook_api = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/setWebhook"
        self.stdout.write(f"New installed webhook {webhook_url} for Telegram")
        requests.post(set_webhook_api, data={"url": webhook_url})
