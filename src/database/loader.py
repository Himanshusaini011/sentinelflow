from src.database.connection import get_connection
from src.utils.logger import logger


def load_security_events(
    logs,
    ingestion_batch_id,
    source_file
):
    """
    Incrementally load valid security events
    into PostgreSQL.

    Existing records are ignored using the
    source file and source row number.
    """

    if logs.empty:
        logger.info(
            "No valid security events to load."
        )
        return 0

    connection = None

    try:

        connection = get_connection()

        inserted_count = 0

        with connection.cursor() as cursor:

            insert_query = """
                INSERT INTO security_events (
                    timestamp,
                    username,
                    source_ip,
                    event_type,
                    status,
                    ingestion_batch_id,
                    source_file,
                    source_row_number
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s
                )
                ON CONFLICT (
                    source_file,
                    source_row_number
                )
                DO NOTHING
            """

            for _, row in logs.iterrows():

                cursor.execute(
                    insert_query,
                    (
                        row["timestamp"],
                        row["user"],
                        row["source_ip"],
                        row["event_type"],
                        row["status"],
                        ingestion_batch_id,
                        source_file,
                        row["source_row_number"]
                    )
                )

                if cursor.rowcount == 1:
                    inserted_count += 1

        connection.commit()

        logger.info(
            f"Inserted {inserted_count} security "
            f"events for batch {ingestion_batch_id}"
        )

        return inserted_count

    except Exception as error:

        if connection:
            connection.rollback()

        logger.error(
            f"Failed to load security events: {error}"
        )

        raise

    finally:

        if connection:
            connection.close()