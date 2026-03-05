import requests
import time

BOT_TOKEN = "8626740595:AAED0Ytf7ikqrrqbn_3zm4LTx15eYyBJvpU"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

offset = 0

def send_message(chat_id,text):
    requests.post(URL+"sendMessage",data={
        "chat_id":chat_id,
        "text":text
    })

while True:
    res = requests.get(URL+"getUpdates",params={"offset":offset}).json()

    for update in res["result"]:
        offset = update["update_id"] + 1

        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text","")

            if text == "/start":
                send_message(chat_id,"Welcome to my bot!")

    time.sleep(2)
