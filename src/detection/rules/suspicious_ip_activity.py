import pandas as pd


def detect(logs):
    """
    Rule 4:
    Detect multiple failed login attempts from the same IP
    targeting multiple different users within one minute.
    """

    threshold = 3
    time_window = pd.Timedelta(minutes=1)

    failed_logins = logs[
        (logs["event_type"] == "LOGIN") &
        (logs["status"] == "FAILED")
    ].copy()

    alerts = []

    for source_ip, group in failed_logins.groupby("source_ip"):

        group = group.sort_values("timestamp")

        for i in range(len(group)):

            start_time = group.iloc[i]["timestamp"]
            end_time = start_time + time_window

            window = group[
                (group["timestamp"] >= start_time) &
                (group["timestamp"] <= end_time)
            ]

            unique_users = window["user"].nunique()

            if len(window) >= threshold and unique_users >= 3:

                actual_end = window.iloc[-1]["timestamp"]

                alerts.append({
                    "source_ip": source_ip,
                    "username": None,
                    "event_count": len(window),
                    "start_time": start_time,
                    "end_time": actual_end,
                    "reason": (
                        "Multiple failed login attempts "
                        "targeting multiple users from the same IP "
                        "within 1 minute"
                    )
                })

                break

    return alerts
