import pandas as pd

from src.detection.rules.failed_then_success import detect


def test_failed_then_success_detected():

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
            "timestamp": "2026-09-27 10:02:00",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "LOGIN",
            "status": "SUCCESS"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "10.0.0.55"
    assert alerts[0]["username"] == "bob"
    assert alerts[0]["event_count"] == 3

def test_failed_logins_without_success_not_detected():

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
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 0