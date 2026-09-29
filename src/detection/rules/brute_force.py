import pandas as pd


def detect(logs):
    """
    Rule 1:
    Detect 5 or more failed login attempts
    from the same IP within one minute.
    """

    threshold = 5
    time_window = pd.Timedelta(minutes=1)

    failed_logins = logs[
        (logs["event_type"] == "LOGIN") &
        (logs["status"] == "FAILED")
    ]

    alerts = []

    for ip, group in failed_logins.groupby("source_ip"):

        group = group.sort_values("timestamp")

        for i in range(len(group)):

            start_time = group.iloc[i]["timestamp"]

            end_time = start_time + time_window

            window = group[
                (group["timestamp"] >= start_time) &
                (group["timestamp"] <= end_time)
            ]

            if len(window) >= threshold:

                actual_end = window.iloc[-1]["timestamp"]

                alerts.append({
                    "source_ip": ip,
                    "username": None,
                    "event_count": len(window),
                    "start_time": start_time,
                    "end_time": actual_end,
                    "reason": (
                        "Multiple failed login attempts "
                        "within 1 minute"
                    )
                })

                break

    return alerts