from database.db import DB
from globals.functions import *


fp = "database/db.sqlite3"
tables = open_json("./database/tables.json")


def data_to_dict(table, data, many=False):
    if many:
        return [{
            k: v for k, v in zip(tables[table], i)
        } for i in data]
    else:
        return {
            k: v for k, v in zip(tables[table], data)
        }


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

    def get_help_requests_by_user_id(self, user_id) -> dict:
        return data_to_dict("help_requests",
                            self.exe("SELECT * FROM help_requests WHERE user_id=?", user_id).fetchall(), many=True)

    def get_help_requests(self, author_id) -> dict:
        user_id = self.get_user_id_by_author_id(author_id)
        return self.get_help_requests_by_user_id(user_id)

    def get_event_by_id(self, event_id) -> dict:
        return data_to_dict("events", self.exe("SELECT * FROM events WHERE id=?", event_id).fetchone())

    def insert_event(self, name, description=None) -> int:
        return self.exe("INSERT INTO events(name, description) VALUES (?, ?, )",
                        name,
                        description
                        ).lastrowid

    def insert_calendar_day(self, event_id, day, day_type):
        return self.exe("INSERT INTO calendar_day(event_id, day, day_type) VALUES (?, ?, ?)",
                        event_id,
                        day,
                        day_type).lastrowid

    def insert_sub_event(self, event_id, name, time_start, time_end, description=None):
        return self.exe(
            "INSERT INTO sub_events(event_id, name, time_start, time_end, description)"
            "VALUES (?, ?, ?, ?, ?, ?)",
            event_id, name, time_start, time_end, description
        )

    def get_event_name_by_id(self, id) -> str:
        res = self.exe("SELECT name FROM events WHERE id=?", id).fetchone()
        if res is None:
            res = [""]
        return res[0]

    def get_event_id_by_name(self, name) -> list:
        return data_to_dict("events", self.exe("SELECT * FROM events WHERE name=?", name).fetchone())

    def get_sub_events_from_event_id(self, event_id) -> list:
        return list(map(lambda x: x[0], self.exe("SELECT id FROM sub_events WHERE event_id=?", event_id).fetchall()))

    def get_sub_events_from_event_name(self, name) -> list:
        event_id = self.get_event_name_by_id(name)
        return self.get_sub_events_from_event_id(event_id)
    
    def get_events_by_time_stamp(self, day_timestamp) -> list:
        return list(map(lambda x: x[0],
                        self.exe("SELECT event_id FROM calendar_day WHERE day=?", day_timestamp).fetchall()))

    def get_events_by_day(self, year, month, day) -> list:
        day_timestamp = datetime.datetime(year, month, day).timestamp()
        return self.get_event_by_time_stamp(day_timestamp)

    def get_days_of_event(self, name) -> list:
        event_id = self.get_event_id_by_name(name)
        return self.get_days_of_event_by_id(event_id)
    
    def get_days_of_event_by_id(self, event_id) -> list:
        return list(map(lambda x: x[0], self.exe("SELECT id FROM calendar_day WHERE event_id=?", event_id).fetchall()))

    def get_days_in_month_by_timestamp(self, month_start_timestamp, month_end_timestamp) -> list:
        return list(map(lambda x: x[0], self.exe("SELECT day FROM calendar_day WHERE day >= ? AND day < ?",
                                                 month_start_timestamp,
                                                 month_end_timestamp).fetchall()))

    def get_days_in_month(self, year, month):
        month_start = datetime.datetime(year, month, 0)
        month_end = datetime.datetime(year, month + 1, 0)
        days_timestamp = self.get_days_in_month_by_timestamp(
            month_start,
            month_end
        )
        timezone = datetime.timezone(datetime.timedelta(hours=3))
        return list(map(lambda x: datetime.datetime.fromtimestamp(x, timezone).day, days_timestamp))
