from globals import *
from telebot import TeleBot

bot = TeleBot(token=creds["helper_token"])


def exec_cond(message, session):
    """
    Conditions when this exact module is used
    returns: boolean -> True: exec() ; False: pass
    """
    if message["text"] == buttons[4 - 1] or session[message["author"]]["state"] in ["help", "help_confirm"]:
        return True
    return False


def execute(message, session):
    """
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
    author = message["author"]
    if session[author]["state"] not in ["help", "help_confirm"]:
        session[author]["state"] = "help"
        return text_message("Возникли проблемы? Хотите задать вопрос администрации? Напишите ваш вопрос."
                            " Он будет отправлен на рассмотрение в чат администрации", author)
    elif session[author]["state"] == "help":
        session[author]["state"] = "help_confirm"
        session[author]["help_text"] = message["text"]
        return text_message_with_keyboard(
                "Вы точно уверены что хотите отправить?",
                ["Да", "Нет"],
                author,
                2
            )

    elif session[author]["state"] == "help_confirm":
        if message["text"] not in ["Да", "Нет"]:
            return text_message_with_keyboard(
                    "Вы точно уверены что хотите отправить?",
                    ["Да", "Нет"],
                    author,
                    2
                )

        session[author]["state"] = "menu"
        if message["text"] == "Да":
            bot.send_message(helper_channel, f"From {message['from']}, {author}: {message['text']}")
            return text_message("Ваше сообщение было успешно доставлено", author)
