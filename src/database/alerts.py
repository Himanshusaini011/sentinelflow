from src.database.connection import get_connection
from src.utils.logger import logger


def save_security_alerts(alerts):
    """
    Store detected security alerts in PostgreSQL.

    Duplicate alerts are ignored using the unique
    constraint on source_ip, start_time, end_time,
    and reason.
    """

    if not alerts:
        logger.info("No security alerts to store.")
        return 0

    connection = None

    try:
        connection = get_connection()

        inserted_count = 0

        with connection.cursor() as cursor:

            insert_query = """
                INSERT INTO security_alerts (
                    source_ip,
                    username,
                    event_count,
                    start_time,
                    end_time,
                    reason
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (
                    source_ip,
                    start_time,
                    end_time,
                    reason
                )
                DO NOTHING
            """

            for alert in alerts:

                cursor.execute(
                    insert_query,
                    (
                        alert["source_ip"],
                        alert["username"],
                        alert["event_count"],
                        alert["start_time"],
                        alert["end_time"],
                        alert["reason"]
                    )
                )

                if cursor.rowcount == 1:
                    inserted_count += 1

        connection.commit()

        logger.info(
            f"Stored {inserted_count} new security alert(s)"
        )

        return inserted_count

    except Exception as error:

        if connection:
            connection.rollback()

        logger.error(
            f"Failed to store security alerts: {error}"
        )

        raise

    finally:

        if connection:
            connection.close()