from database.adapterDB import AdapterDB
from globals.functions import *

db = AdapterDB()
PLATFORMS = ["tg", "vk"]

buttons = open_json("buttons/buttons.json")
creds = open_json("secure/credentials.json")
helper_channel = creds["helper_channel"]
