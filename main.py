import socketio
from aiohttp import web
import os
from globals.globals import *
from globals.functions import *
import sys
import emoji

# Importing everything from folder buttons
sys.path.insert(1, "./buttons")
buttons_mod = {}
current_path = os.path.join(os.getcwd(), "buttons")
for i in os.listdir(current_path):  # Loop through the buttons directory
    if not os.path.isfile(os.path.join(current_path, i)) or\
            i == "buttons.json":  # if file is not file: another directory. Continue
        continue

    module_name = i.replace(".py", "")
    button_name = "_".join(module_name.split("_")[1:])  # First element is just a number
    buttons_mod[button_name] = __import__(module_name)
    # Save the module in buttons dictionary. Example: buttons["schedule"] = <module schedule>
    # So we can access functions and vars through buttons dictionary

socket = socketio.AsyncServer()
app = web.Application()
socket.attach(app)
# Get environmental variable PORT if exists, perhaps use 5000
PORT = os.getenv("PORT", 5000)

session = {}


@socket.event
def connect(sid, environ):
    print(f"connection established with {sid} {environ['REMOTE_ADDR']}")


@socket.event
def disconnect(sid):
    print(f"{sid} disconnected")


@socket.event
async def new_message(sid, data):
    """
    JSON file that represents message sent from user.
    Message must have :
        ["from"], that can be "tg" or "vk"
        ["author"], from tg it must be chat.id, from vk - user_id or chat_id
        ["text"], content of a message as a string, deemojized(emojis replaced with ":emoji_name:" )
    """
    message_obj = data
    try:
        assert message_obj.get("from", None) in PLATFORMS
        assert isinstance(message_obj.get("author", None), int)
        assert isinstance(message_obj.get("text", None), str)
    except AssertionError:
        await socket.emit("error", "400 JSON file requirements were not satisfied", room=sid)
        return
    author = message_obj["author"]

    if not db.get_user_id_by_author_id(author):
        db.insert_user(author, message_obj["from"])
    if author not in session:
        session[author] = {
            "state": "nothing"
        }
    if "state" not in session[author]:
        session["state"] = "nothing"

    # Standard answer
    reply = {
        "user_id": author,
        "type": "text",
        "message": {
            "content": "Команда не найдена. Попробуйте воспользоваться /start"
        }
    }

    # Handling Menu
    if message_obj["text"] == "Меню" or\
            session[author]["state"] == "menu" or\
            message_obj["text"] == "/start":
        reply = text_message_with_keyboard(
            "Добро пожаловать в меню",
            reshape(
                buttons.values(),
                1
            ),
            author
        )
        session["state"] = "nothing"

    # Check the execution conditions of buttons
    for name in buttons_mod:
        button = buttons_mod[name]
        try:
            # exec_cond() function that returns boolean which means is condition met
            if button.exec_cond(message_obj, session):
                reply = button.execute(message_obj, session)  # reply is a ready dictionary to reply
        except Exception as e:
            error_message = e.message if hasattr(e, 'message') else e
            print("Button", button, error_message)
            reply = text_message(f"Произошла ошибка в кнопке {button}: \n{error_message}",
                                 author)

    return await socket.emit("send_message", reply, room=sid)


# If main.py called as "main" file
if __name__ == "__main__":
    # Run the server on PORT
    web.run_app(app, port=PORT)
