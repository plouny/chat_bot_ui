from globals.globals import *

button_help_FAQ_live = ':bed:Проживание'
button_help_FAQ_transfer = ':bus:Трансфер'
button_help_FAQ_food = ':carrot:Питание'


def exec_cond(message: dict, session):
    if message['text'] in [button_help_FAQ_live, button_help_FAQ_transfer, button_help_FAQ_food, buttons["faq"]]:
        return True
    return False


def execute(message, session):
    author = message["author"]
    if message['text'] == button_help_FAQ_live:
        return text_message('''Сбалансированное 5-разовое питание, соответствующее СанПиН''', author)
    elif message['text'] == button_help_FAQ_transfer:
        return text_message(
            '''Обычно трансфер организовывается перед заездом, более подробную информацию вы можете узнать у организаторов''', author)
    elif message['text'] == button_help_FAQ_live:
        return text_message(
            '''Размещение по 2 — 5 человек в светлых, просторных и чистых комнатах кампуса университета''', author)
    else:
        return text_message_with_keyboard('''Вопросы''', [
            [':bed:Проживание', ':bus:Трансфер'],
            [':carrot:Питание', 'Назад в меню'],
        ], author)


