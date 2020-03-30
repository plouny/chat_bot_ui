from .db import DB
from globals.globals import *


fp = "database/db.sqlite3"
tables = open_json("./database/tables.json")


class AdapterDB(DB):
    def __init__(self):
        super().__init__(
            fp,
            tables
        )

    def insert_user(self, author_id, author_from) -> int:
        return self.exe("INSERT INTO users(author_id, author_from) VALUES (?, ?)", author_id, author_from).lastrowid

    def get_user_id_by_author_id(self, author_id) -> int:
        res = self.exe("SELECT id FROM users WHERE author_id=?", author_id).fetchone()
        if res is None:
            return -1
        return res[0]

    def get_author_id_by_user_id(self, user_id) -> int:
        res = self.exe("SELECT author_id FROM users WHERE id=?", user_id).fetchone()
        if res is None:
            return -1
        return res[0]

    def insert_help_request_by_user_id(self, user_id, question) -> int:
        now = get_now_msw()
        return self.exe("INSERT INTO help_requests(user_id, question, time_requested) VALUES (?, ?, ?)",
                        user_id,
                        question,
                        now).lastrowid

    def insert_help_request(self, author_id, question) -> int:
        user_id = self.get_user_id_by_author_id(author_id)
        return self.insert_help_request_by_user_id(user_id, question)

    def get_help_requests_by_user_id(self, user_id) -> list:
        return self.exe("SELECT * FROM help_requests WHERE user_id=?", user_id).fetchall()

    def get_help_requests(self, author_id) -> list:
        user_id = self.get_user_id_by_author_id(author_id)
        return self.get_help_requests_by_user_id(user_id)

    def get_event_by_id(self, event_id) -> list:
        return self.exe("SELECT * FROM events WHERE id=?", event_id).fetchone()

    def insert_event(self, name, description=None, image_filepath=None) -> int:
        return self.exe("INSERT INTO events(name, description, image_filepath) VALUES (?, ?, ?)",
                        name,
                        description,
                        image_filepath).lastrowid

    def insert_calendar_day(self, event_id, day, day_type):
        return self.exe("INSERT INTO calendar_day(event_id, day, day_type) VALUES (?, ?, ?)",
                        event_id,
                        day,
                        day_type).lastrowid

    def insert_sub_event(self, event_id, name, time_start, time_end, description=None, image_filepath=None):
        return self.exe(
            "INSERT INTO sub_events(event_id, name, time_start, time_end, description, image_filepath)"
            "VALUES (?, ?, ?, ?, ?, ?)",
            event_id, name, time_start, time_end, description, image_filepath
        )

    def get_event_name_by_id(self, id) -> str:
        res = self.exe("SELECT name FROM events WHERE id=?", id).fetchone()
        if res is None:
            res = [""]
        return res[0]

    def get_event_id_by_name(self, name) -> list:
        return self.exe("SELECT * FROM events WHERE name=?", name).fetchone()

    def get_sub_events_from_event_id(self, event_id) -> list:
        return list(map(lambda x: x[0], self.exe("SELECT id FROM sub_events WHERE event_id=?", event_id).fetchall()))

    def get_sub_events_from_event_name(self, name) -> list:
        event_id = self.get_event_name_by_id(name)
        return self.get_sub_events_from_event_id(event_id)
    
    def get_event_by_day(self, day_timestamp) -> int:
        res = self.exe("SELECT event_id FROM calendar_day WHERE day=?", day_timestamp).fetchone()
        if res is None:
            res = [-1]
        return res[0]
    
    def get_days_of_event(self, name) -> list:
        event_id = self.get_event_id_by_name(name)
        return self.get_days_of_event_by_id(event_id)
    
    def get_days_of_event_by_id(self, event_id) -> list:
        return list(map(lambda x: x[0], self.exe("SELECT id FROM calendar_day WHERE event_id=?", event_id).fetchall()))
