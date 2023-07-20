import logging

from src.settings import get_settings
from src.clients import DBClient

settings = get_settings()

logger = logging.getLogger(__name__)


def prepare_db() -> None:
    # works
    db_client = DBClient(settings.DB_CONNECTION_URL)

    statement = "SELECT name FROM sqlite_master WHERE type='table' AND name='rates'"
    results = db_client.execute(statement)
    if not results:
        logger.info('Table "rate" not found. Creating a table...')
        _create_db(db_client)


def reset_db() -> None:
    db_client = DBClient(settings.DB_CONNECTION_URL)

    statement = "DROP TABLE rates"
    db_client.execute(statement)
    _create_db(db_client)


def _create_db(db_client: DBClient) -> None:
    statement = """
            CREATE TABLE rates(
                id STRING PRIMARY KEY NOT NULL,
                baseCurrency char(3) NOT NULL,
                currency char(3) NOT NULL,
                rate REAL NOT NULL,
                addDate TIMESTAMP NOT NULL
            )
            """
    db_client.execute(statement)
