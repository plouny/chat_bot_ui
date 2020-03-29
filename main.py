from flask import Flask, request, jsonify, abort
import os
from globals import *
import sys

# Importing everything from folder buttons
sys.path.insert(1, "./buttons")
buttons = {}
current_path = os.path.join(os.getcwd(), "buttons")
for i in os.listdir(current_path):  # Loop through the buttons directory
    if not os.path.isfile(os.path.join(current_path, i)) or\
            i == "buttons.json":  # if file is not file: another directory. Continue
        continue

    module_name = i.replace(".py", "")
    button_name = "_".join(module_name.split("_")[1:])  # First element is just a number
    buttons[button_name] = __import__(module_name)
    # Save the module in buttons dictionary. Example: buttons["schedule"] = <module schedule>
    # So we can access functions and vars through buttons dictionary

app = Flask(__name__)
# Get environmental variable PORT if exists, perhaps use 5000
PORT = os.getenv("PORT", 5000)

PLATFORMS = ["tg", "vk"]
session = {}


@app.route("/handle_message", methods=["POST"])
def handle_message():
    """
    JSON file that represents message sent from user.
    Message must have :
        ["from"], that can be "tg" or "vk"
        ["author"], from tg it must be chat.id, from vk - user_id or chat_id
        ["text"], content of a message as a string, deemojized(emojis replaced with ":emoji_name:" )
    """
    message = request.json
    try:
        assert message.get("from", None) in PLATFORMS
        assert isinstance(message.get("author", None), int)
        assert isinstance(message.get("text", None), str)
    except AssertionError:
        abort(400, "JSON file requirements were not satisfied")
    author = message["author"]
    if not db.get_user_id_by_author_id(author):
        db.insert_user(author)
    if author not in session:
        session[author] = {
            "state": "menu"
        }
    if "state" not in session[author]:
        session["state"] = "menu"
    reply = {
        "type": "text",
        "message": "Команда не найдена. Попробуйте воспользоваться /help"
    }
    # Check the execution conditions of buttons
    for name in buttons:
        button = buttons[name]
        if button.exec_cond(message, session):  # exec_cond() function that returns boolean which means is condition met
            reply = button.execute(message, session)  # reply is a ready dictionary to reply

    return jsonify(reply)


# If main.py called as "main" file
if __name__ == "__main__":
    # Run the server on PORT
    app.run("0.0.0.0", PORT, threaded=True)
