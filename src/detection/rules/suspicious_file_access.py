import pandas as pd


def detect(logs):
    """
    Detect unusually frequent FILE_ACCESS events
    from the same user within one minute.
    """

    threshold = 5
    time_window = pd.Timedelta(minutes=1)

    file_access = logs[
        logs["event_type"] == "FILE_ACCESS"
    ].copy()

    alerts = []

    for username, group in file_access.groupby("user"):

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
                    "source_ip": window.iloc[0]["source_ip"],
                    "username": username,
                    "event_count": len(window),
                    "start_time": start_time,
                    "end_time": actual_end,
                    "reason": "Suspicious frequency of file access within 1 minute"
                })

                break

    return alerts