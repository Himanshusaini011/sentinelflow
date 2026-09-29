import pandas as pd


def transform_security_logs(logs):
    """
    Clean and transform security log data.
    """

    # Convert timestamp from string to datetime
    # Invalid timestamps become NaT instead of crashing
    logs["timestamp"] = pd.to_datetime(
        logs["timestamp"],
        errors="coerce"
    )

    # Sort records by timestamp
    logs = logs.sort_values("timestamp")

    # Reset DataFrame index
    logs = logs.reset_index(drop=True)

    return logs