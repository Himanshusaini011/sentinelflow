from src.database.connection import get_connection
from src.utils.logger import logger


def load_quarantined_events(
    records,
    source_file
):
    """
    Incrementally store invalid security events.
    """

    if not records:
        logger.info(
            "No records require quarantine."
        )
        return 0

    connection = None

    try:

        connection = get_connection()

        inserted_count = 0

        with connection.cursor() as cursor:

            insert_query = """
                INSERT INTO security_event_quarantine (
                    timestamp,
                    username,
                    source_ip,
                    event_type,
                    status,
                    issue_type,
                    issue_description,
                    source_file,
                    source_row_number
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                ON CONFLICT (
                    source_file,
                    source_row_number
                )
                DO NOTHING
            """

            for record in records:

                cursor.execute(
                    insert_query,
                    (
                        record["timestamp"],
                        record["username"],
                        record["source_ip"],
                        record["event_type"],
                        record["status"],
                        record["issue_type"],
                        record["issue_description"],
                        source_file,
                        record["source_row_number"]
                    )
                )

                if cursor.rowcount == 1:
                    inserted_count += 1

        connection.commit()

        logger.warning(
            f"Quarantined {inserted_count} "
            f"new invalid record(s)"
        )

        return inserted_count

    except Exception as error:

        if connection:
            connection.rollback()

        logger.error(
            f"Failed to load quarantine records: {error}"
        )

        raise

    finally:

        if connection:
            connection.close()