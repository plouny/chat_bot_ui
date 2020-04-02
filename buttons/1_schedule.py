from globals.globals import *
from datetime import datetime
import datetime as date


def get_days():
    kazan_tz = date.timezone(date.timedelta(hours=3))
    today = date.datetime.now().astimezone(tz=kazan_tz).timestamp()
    day = 24*3600
    days = [today, today + day, today + (day*2)]
    days = list(map(lambda x: datetime.fromtimestamp(x).strftime("%d/%m"), days))
    return days


def exec_cond(message, session):
    """ TODO
    Conditions when this exact module is used
    returns: boolean -> True: exec() ; False: pass
    """
    if message["text"] == buttons["schedule"]:
        return True
    elif message["text"] in get_days():
        session["state"] = states["schedule"]
        return True
    else:
        return False


def execute(message, session):
    """ TODO
       Execution of giving answer to message
       returns: !!!LIST!!! of messages
       message must be in format:
           {
               "user_id": who will receive this message. If None -> return this message to the author
               "type": "text"/"keyboard"/"image",
               "message": {
                   "content": text_content,
                   "image_id": image_id, # Exist only when type == image
                   "keyboard_buttons": ["option1", "option2", ..], # Exist only when type == keyboard
                   "row_width": row_width  # Exist only when type == keyboard
               }
           }
       """
    if session["state"] == states["nothing"]:
        ans = {"user_id": None, "type": "keyboard", "message": {"content": buttons["schedule"],
                                                                "keyboard_buttons": get_days()}}
        messages_list = [ans]
        return messages_list
    elif session["state"] == states["schedule"]:
        text = message["text"]
        ans = {"user_id": None, "type": "text", "message": {"content": "".join(list(map(
            lambda x: x + "\n", db.get_event_by_day(text))))}}
        messages_list = [ans]
        return messages_list


