import pandas as pd


def detect(logs):
    """
    Rule 2:
    Detect multiple failed login attempts followed
    by a successful login from the same user and IP.
    """

    threshold = 3
    time_window = pd.Timedelta(minutes=5)

    login_events = logs[
        logs["event_type"] == "LOGIN"
    ].copy()

    alerts = []

    for (username, source_ip), group in login_events.groupby(
        ["user", "source_ip"]
    ):

        group = group.sort_values("timestamp")

        failed_events = group[
            group["status"] == "FAILED"
        ]

        successful_events = group[
            group["status"] == "SUCCESS"
        ]

        for _, success in successful_events.iterrows():

            success_time = success["timestamp"]

            previous_failures = failed_events[
                (failed_events["timestamp"] < success_time) &
                (
                    failed_events["timestamp"]
                    >= success_time - time_window
                )
            ]

            if len(previous_failures) >= threshold:

                start_time = previous_failures.iloc[0]["timestamp"]

                alerts.append({
                    "source_ip": source_ip,
                    "username": username,
                    "event_count": len(previous_failures),
                    "start_time": start_time,
                    "end_time": success_time,
                    "reason": (
                        "Multiple failed login attempts "
                        "followed by successful login"
                    )
                })

                break

    return alerts