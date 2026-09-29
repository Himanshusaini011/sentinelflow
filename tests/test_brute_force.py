import pandas as pd

from src.detection.rules.brute_force import detect


def test_brute_force_detected():
    logs = pd.DataFrame([
        {
            "timestamp": "2026-09-27 10:01:11",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:14",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:17",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:20",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:23",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "LOGIN",
            "status": "FAILED"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "10.0.0.55"
    assert alerts[0]["event_count"] == 5