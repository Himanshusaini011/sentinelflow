from datetime import datetime

from src.database.connection import get_connection
from src.utils.logger import logger


def start_ingestion_run(batch_id, source_file, records_received):
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            query = """
                INSERT INTO ingestion_runs (
                    batch_id,
                    source_file,
                    started_at,
                    records_received,
                    status
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    batch_id,
                    source_file,
                    datetime.now(),
                    records_received,
                    "RUNNING"
                )
            )

        connection.commit()

    except Exception as error:

        if connection:
            connection.rollback()

        logger.error(
            f"Failed to start ingestion run: {error}"
        )

        raise

    finally:

        if connection:
            connection.close()


def update_records_received(batch_id, records_received):
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            query = """
                UPDATE ingestion_runs
                SET records_received = %s
                WHERE batch_id = %s
            """

            cursor.execute(
                query,
                (
                    records_received,
                    batch_id
                )
            )

        connection.commit()

    except Exception as error:

        if connection:
            connection.rollback()

        logger.error(
            f"Failed to update records received: {error}"
        )

        raise

    finally:

        if connection:
            connection.close()


def complete_ingestion_run(
    batch_id,
    records_loaded,
    records_quarantined,
    status="SUCCESS"
):
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            query = """
                UPDATE ingestion_runs
                SET
                    completed_at = %s,
                    records_loaded = %s,
                    records_quarantined = %s,
                    status = %s
                WHERE batch_id = %s
            """

            cursor.execute(
                query,
                (
                    datetime.now(),
                    records_loaded,
                    records_quarantined,
                    status,
                    batch_id
                )
            )

        connection.commit()

    except Exception as error:

        if connection:
            connection.rollback()

        logger.error(
            f"Failed to complete ingestion run: {error}"
        )

        raise

    finally:

        if connection:
            connection.close()