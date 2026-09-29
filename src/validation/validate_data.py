import ipaddress
import pandas as pd


def validate_security_logs(logs):
    """
    Validate security logs and separate
    valid and invalid records.
    """

    valid_event_types = {
        "LOGIN",
        "LOGOUT",
        "FILE_ACCESS"
    }

    valid_status = {
        "SUCCESS",
        "FAILED"
    }

    valid_records = []
    quarantined_records = []

    required_columns = [
        "timestamp",
        "user",
        "source_ip",
        "event_type",
        "status",
        "source_row_number"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in logs.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    for index, row in logs.iterrows():

        issues = []

        # Validate timestamp
        if pd.isna(row["timestamp"]):
            issues.append(
                "Invalid or missing timestamp"
            )

        # Validate username
        if (
            pd.isna(row["user"])
            or not str(row["user"]).strip()
        ):
            issues.append(
                "Missing username"
            )

        # Validate IP address
        try:
            ipaddress.ip_address(
                str(row["source_ip"])
            )
        except ValueError:
            issues.append(
                "Invalid IP address"
            )

        # Validate event type
        if row["event_type"] not in valid_event_types:
            issues.append(
                "Invalid event type"
            )

        # Validate status
        if row["status"] not in valid_status:
            issues.append(
                "Invalid status"
            )

        # Separate invalid records
        if issues:

            quarantined_records.append({
                "timestamp": str(row["timestamp"]),
                "username": str(row["user"]),
                "source_ip": str(row["source_ip"]),
                "event_type": str(row["event_type"]),
                "status": str(row["status"]),
                "source_row_number": int(
                    row["source_row_number"]
                ),
                "issue_type": "DATA_QUALITY",
                "issue_description": "; ".join(issues)
            })

        else:
            valid_records.append(index)

    valid_logs = logs.loc[
        valid_records
    ].copy()

    return valid_logs, quarantined_records