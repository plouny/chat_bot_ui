import sqlite3
import functools


# Decorator that updates connection and cursor. It used on functions that in functions_needed_to_be_update
def update_conn(s):
    def f(fun):
        @functools.wraps(fun)
        def wrapped(*args, **kwargs):
            conn = sqlite3.connect(s.path)
            cursor = conn.cursor()
            result = fun(cursor, *args, **kwargs)
            conn.commit()
            return result

        return wrapped

    return f


functions_needed_to_be_update = [
    "ready_tables",
    "exe"
]


class DB:
    def __init__(self, filepath: str, tables: dict) -> None:
        self.path = filepath
        self.tables = tables

        method_list = [func for func in dir(DB)]
        for i, method in enumerate(method_list):
            if callable(getattr(DB, method)) and not method.startswith("__") \
                    and method in functions_needed_to_be_update:
                setattr(self, method, update_conn(self)(getattr(self, method)))
        # ---------------------------------------------------------------------------
        self.ready_tables()

    def ready_tables(self, cursor: sqlite3.Cursor) -> None:
        for table in self.tables:
            schema = list(map(lambda k: k + " " + self.tables[table][k], self.tables[table]))
            try:
                cursor.execute(
                    f"CREATE TABLE {table}({','.join(schema)})"
                )
            except Exception as e:
                pass  # table already exists

    def exe(self, cursor: sqlite3.Cursor, s: str, *args) -> sqlite3.Cursor:
        return cursor.execute(s, args)
