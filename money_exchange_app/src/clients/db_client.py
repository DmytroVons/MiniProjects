import logging
import sqlite3
from typing import Self

logger = logging.getLogger(__name__)


class DBOperationError(Exception):
    pass


class DBContextManager:

    def __init__(self, url: str) -> None:
        self._url = url
        self._connection = None

    def __enter__(self) -> sqlite3.Cursor:
        self._connection = sqlite3.connect(self._url)
        return self._connection.cursor()

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb) -> bool:
        self._connection.close()
        if exc_type:
            msg = f'SQL operaion error. Error: {exc_type}: {exc_val}'
            logger.error(msg)
            raise DBOperationError(msg)

        return False


class DBClient:
    _instance: Self = None

    def __new__(cls, *args, **kwargs) -> 'DBClient':
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, connect_url: str) -> None:
        self._connect_url = connect_url

    def execute(self, statement: str, values: tuple | None = None) -> list[tuple] | None:
        with DBContextManager(self._connect_url) as cursor:
            if values:
                # write operations
                ex_res = cursor.execute(statement, values)
                cursor.connection.commit()
            else:
                # read operations
                ex_res = cursor.execute(statement)
            res = ex_res.fetchall()

        return res

    def executemany(self, statement: str, values: list[tuple]) -> list[tuple]:
        with DBContextManager(self._connect_url) as cursor:
            res = cursor.executemany(statement, values)
            cursor.connection.commit()
            res = res.fetchall()
        return res
