import pandas as pd

from src.detection.rules.suspicious_ip_activity import detect


def test_suspicious_ip_activity_detected():

    logs = pd.DataFrame([
        {
            "timestamp": "2026-09-27 10:00:01",
            "user": "alice",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:00:10",
            "user": "bob",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:00:20",
            "user": "charlie",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "10.0.0.50"
    assert alerts[0]["event_count"] == 3
    assert alerts[0]["username"] is None


def test_same_user_does_not_trigger():

    logs = pd.DataFrame([
        {
            "timestamp": "2026-09-27 10:00:01",
            "user": "alice",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:00:10",
            "user": "alice",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:00:20",
            "user": "alice",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 0


def test_different_users_outside_time_window():

    logs = pd.DataFrame([
        {
            "timestamp": "2026-09-27 10:00:01",
            "user": "alice",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:30",
            "user": "bob",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:03:00",
            "user": "charlie",
            "source_ip": "10.0.0.50",
            "event_type": "LOGIN",
            "status": "FAILED"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 0
