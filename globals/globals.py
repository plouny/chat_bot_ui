from database.adapterDB import AdapterDB
from globals.functions import *

db = AdapterDB()

buttons: dict = open_json("buttons/buttons.json")
creds: dict = open_json("secure/credentials.json")
helper_channel = creds["helper_channel"]
states: dict = open_json("buttons/states.json")
