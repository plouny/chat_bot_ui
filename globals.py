import json
import datetime
from database.adapterDB import AdapterDB

db = AdapterDB()
PLATFORMS = ["tg", "vk"]


def open_json(fp):
    with open(fp, encoding="UTF8") as f:
        return json.load(f)


def get_now_msw():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3)


def text_message(text, author):
    return {
        "user_id": author,
        "type": "text",
        "message": {
            "content": text
        }
    }


def text_message_with_keyboard(text, keyboard_buttons, author, rows=5):
    return {
        "user_id": author,
        "type": "keyboard",
        "message": {
            "content": text,
            "keyboard_buttons": keyboard_buttons,
            "rows": rows
        }
    }


buttons = open_json("buttons/buttons.json")
creds = open_json("secure/credentials.json")
helper_channel = creds["helper_channel"]
