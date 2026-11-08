import hmac
import hashlib
import time
import json
import requests
import uuid
from config import settings
# --- НАСТРОЙКИ ---
SECRET = settings.BITSBY_WEBHOOK_SECRET
USER_ID = settings.USER_ID # Твой реальный Telegram ID
SERVER_URL = settings.BITSBY_WEBHOOK_URL

def send_fake_webhook():
    # 1. Формируем тело запроса (как будто Bitsby прислал оплату)
    payload = {
        "invoice": {
            "id": str(uuid.uuid4()),
            "status": "paid",
            "serviceData": json.dumps({"user_id": USER_ID,"duration": 99})
        }
    }
    # Переводим словарь в строку JSON
    raw_body = json.dumps(payload, separators=(',', ':'))

    # 2. Генерируем время
    timestamp = str(int(time.time()))

    # 3. Вычисляем подпись (HMAC SHA256)
    expected_sig = "sha256=" + hmac.new(
        SECRET.encode(),
        f"{timestamp}.{raw_body}".encode(),
        hashlib.sha256
    ).hexdigest()

    # 4. Отправляем запрос на сервер
    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": timestamp,
        "X-Signature": expected_sig
    }

    print(f"Отправляем запрос на {SERVER_URL}...")
    print(f"Подпись: {expected_sig}")

    try:
        response = requests.post(SERVER_URL, data=raw_body, headers=headers)
        print(f"Ответ сервера: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    send_fake_webhook()