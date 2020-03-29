from .db import DB
import json


def open_json(fp):
    with open(fp) as f:
        return json.load(f)


fp = "database/db.sqlite3"
tables = open_json("./database/tables.json")


class AdapterDB(DB):
    def __init__(self):
        super().__init__(
            fp,
            tables
        )

    def insert_user(self, author_id):
        self.exe("INSERT INTO users(author_id) VALUES (?)", author_id)

    def get_user_id_by_author_id(self, author_id):
        res = self.exe("SELECT id FROM users WHERE author_id=?", author_id).fetchone()
        if res is None:
            return []
        return res[0]

    def get_author_id_by_user_id(self, user_id):
        res = self.exe("SELECT author_id FROM users WHERE id=?", user_id).fetchone()
        if res is None:
            return []
        return res[0]

    def insert_help_request_by_user_id(self, user_id, question):
        now = get_now_msw()
        self.exe("INSERT INTO help_requests(user_id, question, time_requested) VALUES (?, ?, ?)", user_id, question, now)

    def insert_help_request(self, author_id, question):
        user_id = self.get_user_id_by_author_id(author_id)
        self.insert_help_request_by_user_id(user_id, question)

    def get_help_requests_by_user_id(self, user_id):
        return self.exe("SELECT * FROM help_requests WHERE user_id=?", user_id).fetchall()

    def get_help_requests(self, author_id):
        user_id = self.get_user_id_by_author_id(author_id)
        return self.get_help_requests_by_user_id(user_id)

