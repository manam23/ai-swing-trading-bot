import os
import requests

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    return response.json()


if __name__ == "__main__":

    send_telegram_alert(
        "🚀 AI Swing Trading Bot Connected Successfully!"
    )