from globals.functions import *
from globals.globals import *


def exec_cond(message, session):
    return message["text"].strip() in ['contacts', buttons["contacts"]]


def execute(message, session):
    """
    Execution of giving answer to message
    returns: !!!LIST!!! of messages
    message must be in format:
        {
            "type": "text"/"keyboard"/"image",
            "message": {
                "content": text_content/ ["option1", "option2", ..]/image_id,
                "row_width": row_width  # Exist only when type == keyboard
            }
        }
    """
    text = (':phone: Контакты \n' +
            ':house: Наш адрес: Университетская ул., 1, Иннополис\n' +
            ':telephone_receiver: Наш телефон: +7(843)203-92-53\n' +
            ':globe_with_meridians: Наш сайт: university.innopolis.ru\n' +
            ':email:Наш email: university@innopolis.ru\n' +
            ':clock9:Наш режим работы: пн-пт 9:00–18:00')

    return text_message(text, message["author"])
