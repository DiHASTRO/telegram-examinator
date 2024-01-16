import sqlite3 as sql

from pathlib import Path

from . import settings
from . import sql_constants


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(object, metaclass=SingletonMeta):
    _connection = None

    @property
    def _conn(self):
        if not Path(settings.DATABASE_PATH).exists():
            self._create_database(settings.DATABASE_PATH)
        elif self._connection is None:
            self._connection = sql.connect(settings.DATABASE_PATH)

        return self._connection

    @property
    def _cur(self):
        pass

    def close(self):
        if self._connection is not None:
            self._connection.close()

    def _create_database(self, path: str) -> None:
        self._connection = sql.connect(path)
        cur = self._connection.cursor()
        try:
            for query in sql_constants.TABLES_INIT_QUERIES.values():
                cur.execute(query)
            self._connection.commit()
            cur.close()
        except Exception as e:
            cur.close()
            raise e

    def _insert_user(self, user_tuple: tuple) -> None:
        with CursorWrapper(self._conn) as cur:
            cur.execute(sql_constants.INSERT_QUERIES['users'], user_tuple)
            self._conn.commit()


class CursorWrapper(object):

    def __init__(self, conn: sql.Connection, *args, **kwargs):
        self.conn = conn
        self.args = args
        self.kwargs = kwargs
    
    def __enter__(self) -> sql.Cursor:
        self.cursor = self.conn.cursor(*self.args, *self.kwargs)
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, tb) -> True:
        self.cursor.close()

        if exc_type is not None:
            return False

        return True
