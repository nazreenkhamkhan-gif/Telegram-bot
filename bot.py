import requests
import time
import random
from datetime import datetime

BOT_TOKEN = "8626740595:AAHijSCWofzmYKpFglxQrQYnUaUGaVJzN60"

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

users = set()

ADMIN_ID = 123456789


def send_message(chat_id, text):

    url = BASE_URL + "/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, data=data)


def get_updates(offset=None):

    url = BASE_URL + "/getUpdates"

    params = {
        "timeout": 100,
        "offset": offset
    }

    r = requests.get(url, params=params)

    return r.json()


offset = None


while True:

    updates = get_updates(offset)

    if "result" in updates:

        for update in updates["result"]:

            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            chat_id = update["message"]["chat"]["id"]

            text = update["message"].get("text", "")

            users.add(chat_id)

            # start
            if text == "/start":

                send_message(chat_id,
                "🤖 Welcome to Utility Bot\nUse /help")

            # help
            elif text == "/help":

                send_message(chat_id,
"""
📋 Commands

/start
/help
/about
/calc
/time
/date
/echo
/pincode
/ip
/number
/imei
/qr
/random
/password
/ping
/users
/buy
/premium
""")

            # calculator
            elif text.startswith("/calc"):

                try:

                    exp = text.replace("/calc ", "")

                    result = eval(exp)

                    send_message(chat_id,
                    f"🧮 Result: {result}")

                except:

                    send_message(chat_id,
                    "❌ Invalid")

            # time
            elif text == "/time":

                now = datetime.now().strftime("%H:%M:%S")

                send_message(chat_id,
                f"⏰ Time: {now}")

            # random number
            elif text == "/random":

                num = random.randint(1,100)

                send_message(chat_id,
                f"🎲 Random: {num}")

            # password
            elif text == "/password":

                chars = "abcdefghijklmnopqrstuvwxyz123456789"

                pwd = "".join(random.choice(chars) for i in range(10))

                send_message(chat_id,
                f"🔐 Password: {pwd}")

            # ping
            elif text == "/ping":

                send_message(chat_id,
                "🏓 Pong")

            # users
            elif text == "/users":

                send_message(chat_id,
                f"👥 Users: {len(users)}")

    time.sleep(2)
