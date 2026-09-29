import os

import psycopg
from dotenv import load_dotenv

from src.utils.logger import logger


load_dotenv()


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    host = os.getenv("SENTINELFLOW_DB_HOST", "localhost")
    port = os.getenv("SENTINELFLOW_DB_PORT", "5432")
    dbname = os.getenv("SENTINELFLOW_DB_NAME", "sentinelflow")
    user = os.getenv("SENTINELFLOW_DB_USER", "postgres")
    password = os.getenv("SENTINELFLOW_DB_PASSWORD")

    if not password:
        raise RuntimeError(
            "SENTINELFLOW_DB_PASSWORD is not configured"
        )

    try:

        connection = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )

        logger.info(
            "PostgreSQL connection established"
        )

        return connection

    except Exception as error:

        logger.error(
            f"PostgreSQL connection failed: {error}"
        )

        raise