import sqlite3 as sql
from pathlib import Path

from . import logging_config
import logging

logger = logging.getLogger(__name__)

from . import settings
from . import sql_constants


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            logger.debug(f"Added singleton to {cls}")
        return cls._instances[cls]


class Database(object, metaclass=SingletonMeta):
    _connection = None

    @property
    def _conn(self):
        try:
            if not Path(settings.DATABASE_PATH).exists():
                self._create_database(settings.DATABASE_PATH)
            elif self._connection is None:
                self._connection = sql.connect(settings.DATABASE_PATH)
                logger.info(f'Connected to database')
        except Exception as e:
            logger.critical(f'Failed to connect to database: {e}', exc_info=True)
            raise e

        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            logger.info(f'Database connection is closed')

    def _create_database(self, path: str) -> None:
        logger.debug(f'Creating database with path "{path}" ...')
        self._connection = sql.connect(path)
        cur = self._connection.cursor()
        try:
            logger.debug(f'Adding tables and constraints ...')
            for query in sql_constants.TABLES_INIT_QUERIES.values():
                logger.debug(f'SQL query: {query}')
                cur.execute(query)
            self._connection.commit()
        finally:
            cur.close()
        logger.info(f"Databased created succesfully with path {path}")

    def _insert_user(self, names_values: list) -> None:
        logger.debug(f'Inserting user into database with values: {dict(map(lambda k, v : (k, v), *names_values))} ...')
        with CursorWrapper(self._conn) as cur:
            query = sql_constants.INSERT_QUERIES['users'].format(*names_values)
            logger.debug(f'SQL query: {query}')
            cur.execute(query)
            self._conn.commit()
        logger.info(f'User inserted successfully into database with values: {names_values}')

    def _get_user_data_by_id(self, id: int) -> tuple:
        logger.debug(f'Getting user data by database id = {id}')
        with CursorWrapper(self._conn) as cur:
            query = sql_constants.SELECT_QUERIES['get_user_by_id'].format(id)
            logger.debug(f'SQL query: {query}')
            res = cur.execute(query)
            data = res.fetchone()
            if data is None:
                logger.warning(f'User with id = {id} does not exist')
        logger.info(f'Succesfully gotten user data from database with id = {id}')
        
        return data 

class CursorWrapper(object):

    def __init__(self, conn: sql.Connection, *args, **kwargs):
        self.conn = conn
        self.args = args
        self.kwargs = kwargs
    
    def __enter__(self) -> sql.Cursor:
        self.cursor = self.conn.cursor(*self.args, *self.kwargs)
        logger.debug(f"Cursor opened to connection {self.conn}")
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, tb) -> True:
        self.cursor.close()
        logger.debug(f"Cursor closed to connection {self.conn}")

        if exc_type is not None:
            logger.warning(f"Exception with cursor occured: {exc_value}")
        return exc_type is None
