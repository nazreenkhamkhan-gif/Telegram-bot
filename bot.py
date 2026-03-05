import requests
import time
import sqlite3

BOT_TOKEN = "8626740595:AAHijSCWofzmYKpFglxQrQYnUaUGaVJzN60"
ADMIN_ID = 5909895493
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, premium INTEGER)")
conn.commit()

offset = 0

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, premium) VALUES (?,0)", (user_id,))
    conn.commit()

def get_user_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]

def set_premium(user_id):
    cursor.execute("UPDATE users SET premium=1 WHERE user_id=?", (user_id,))
    conn.commit()

def is_premium(user_id):
    cursor.execute("SELECT premium FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == 1

def broadcast(message):
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    for u in users:
        try:
            send_message(u[0], message)
        except:
            pass

while True:
    res = requests.get(URL + "getUpdates", params={"offset": offset}).json()

    for update in res["result"]:
        offset = update["update_id"] + 1

        if "message" in update:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")
            user_id = msg["from"]["id"]

            add_user(user_id)

            if text == "/start":
                send_message(chat_id, "👋 Welcome!\nUse /help")

            elif text == "/help":
                send_message(chat_id, "/start\n/help\n/id\n/premium\n/tool")

            elif text == "/id":
                send_message(chat_id, f"Your ID: {user_id}")

            elif text == "/premium":
                send_message(chat_id, "Premium ₹49\nUPI: yourupi@upi\nPayment ke baad admin ko screenshot bhejo")

            elif text == "/tool":
                if is_premium(user_id):
                    send_message(chat_id, "🔓 Premium tool access granted")
                else:
                    send_message(chat_id, "❌ Premium required")

            elif text == "/stats":
                if user_id == ADMIN_ID:
                    send_message(chat_id, f"Users: {get_user_count()}")

            elif text.startswith("/broadcast"):
                if user_id == ADMIN_ID:
                    message = text.replace("/broadcast", "")
                    broadcast(message)
                    send_message(chat_id, "Broadcast sent")

            elif text.startswith("/addpremium"):
                if user_id == ADMIN_ID:
                    try:
                        uid = int(text.split()[1])
                        set_premium(uid)
                        send_message(chat_id, "Premium added")
                    except:
                        send_message(chat_id, "Usage: /addpremium user_id")

    time.sleep(2)
