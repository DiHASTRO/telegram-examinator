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
            with CursorWrapper(self._connection) as cur:
                cur.execute(sql_constants.PRAGMA_QUERIES['turn_foreign_keys_on'])
                self._connection.commit()
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
                cur.execute(query)
            self._connection.commit()
        finally:
            cur.close()
        logger.info(f"Databased created succesfully with path {path}")

    def _insert_in_table(self, table: str, names_values: list) -> None:
        logger.debug(f'Inserting {table} database with values: {dict(map(lambda k, v : (k, v), *names_values))} ...')
        with CursorWrapper(self._conn) as cur:
            query = sql_constants.INSERT_QUERIES['common_insert'].format(table, *names_values)
            cur.execute(query)
            self._conn.commit()
        logger.info(f'Inserted successfully into \'{table}\' with values: {names_values}')

    def _get_table_data_by_column(self, table: str, column: str, value) -> tuple:
        logger.debug(f'Getting data from \'{table}\' with {column} = {value}...')
        with CursorWrapper(self._conn) as cur:
            query = sql_constants.SELECT_QUERIES['get_by_column'].format(table, column, value)
            res = cur.execute(query)
            
            data = res.fetchone()
            if data is None:
                logger.warning(f'Row in \'{table}\' with {column} = {value} does not exist')
            else:
                logger.info(f'Succesfully gotten data from \'{table}\' with {column} = {value}')
        
        return data

    def _delete_table_data_by_column(self, table: str, column: str, value):
        logger.debug(f'Deleting data from \'{table}\' with {column} = {value}')
        with CursorWrapper(self._conn) as cur:
            query = sql_constants.DELETE_QUERIES['delete_by_column'].format(table, column, value)

            res = cur.execute(query)
            self._conn.commit()

        if res.rowcount == 0:
            logger.warning(f'Row in \'{table}\' with {column} = {value} does not exist. Nothing has been deleted')
        else:
            logger.info(f'Deleted successfully from \'{table}\' {res.rowcount} items')
        return res.rowcount


class CursorWrapper(sql.Cursor):
    def __init__(self, conn: sql.Connection, *args, **kwargs):
        super().__init__(conn, *args, **kwargs)
        self.conn = conn
        logger.debug(f"Cursor opened to connection {self.conn}")
        
    def __enter__(self) -> sql.Cursor:
        return self
    
    def __exit__(self, exc_type, exc_value, tb) -> True:
        self.close()
        logger.debug(f"Cursor closed to connection {self.conn}")

        if exc_type is not None:
            logger.warning(f"Exception with cursor occured: {exc_value}")
        return exc_type is None

    def execute(self, __sql: str, __parameters: list = ()):
        logger.debug(f'SQL query: {__sql} {f"with parameters {__parameters}" if __parameters else ""}')
        try:
            exec_result = super().execute(__sql, __parameters)
        except Exception as e:
            logger.critical(f'Failed to execute cursor command: {e}', exc_info=True)
            raise e
        return exec_result
