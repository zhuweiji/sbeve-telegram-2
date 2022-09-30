import httpx

from dataclasses import dataclass
import logging
import os

from src.services.utilities import TOKEN, WEBHOOK_URL

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

TELEGRAM_URL = "https://api.telegram.org/bot"


def establish_webhook(uri:str = ""):
    url = WEBHOOK_URL + uri
    log.info(f"Webhook URL: {url}")

    result = httpx.get(f"{TELEGRAM_URL}{TOKEN}/setWebhook?url={url}")
    log.info(f"Set webhook result: {result.status_code}")
    log.info(result.text)
    return result.status_code == 200
