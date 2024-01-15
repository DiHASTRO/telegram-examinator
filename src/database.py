import sqlite3 as sql

from pathlib import Path
import settings

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(object, metaclass=SingletonMeta):
    @property
    def conn(self):
        if not Path(settings.DATABASE_PATH).exists():
            self.__create_database()

        return self.__connection


    def __create_database(self):
        self._connection = sql.connect(settings.DATABASE_PATH)
