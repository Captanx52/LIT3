import os
import sqlite3

class LIT3:
    def __init__(self, name: str, path: str = "") -> None:
        self.name = name
        self.path = os.path.join(path, f"{name}.db")
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()
        self.tables = []



    def add_table(self, instance):
        table_name = instance.__name__
        columns = ", ".join([f"{attr_name} {self.get_sqlite_type(attr_type)}" for attr_name, attr_type in instance.__annotations__.items()])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        self.cur.execute(create_table_query)
        self.conn.commit()
        self.tables.append(table_name)

    def get_sqlite_type(self, py_type):
        if py_type == int:
            return "INTEGER"
        elif py_type == str:
            return "TEXT"
        elif py_type == float:
            return "REAL"
        elif py_type == bool:
            return "BOOLEAN"
        else:
            return "TEXT"

    def add_session(self, instance):
        table_name = instance.__class__.__name__
        columns = ", ".join(instance.__annotations__.keys())
        placeholders = ", ".join(["?"] * len(instance.__annotations__))
        values = tuple(getattr(instance, attr) for attr in instance.__annotations__.keys())
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cur.execute(insert_query, values)
        self.conn.commit()
        
        
    def __del__(self):
        self.conn.close()