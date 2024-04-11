import sqlite3
from sqlite3 import Connection as SqliteCoon


class Connection:

    _instance: "Connection" = None  # type: ignore
    __coon = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        try:
            print("connectando")
            self._instance.__coon = sqlite3.connect(
                "database.db", check_same_thread=False
            )
        except Exception as e:
            print(e)

    def close(self):
        if not self._instance.__coon:
            return
        self._instance.close()

    def get_database(self) -> SqliteCoon:
        if not self._instance.__coon:
            self.connect()
        return self._instance.__coon  # type: ignore

    def get_new_connection(self):
        return sqlite3.connect("database.db", check_same_thread=False)
