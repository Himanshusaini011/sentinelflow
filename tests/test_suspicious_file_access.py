import pandas as pd

from src.detection.rules.suspicious_file_access import detect


def test_suspicious_file_access_detected():

    logs = pd.DataFrame([
        {
            "timestamp": "2026-09-27 10:01:01",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 10:01:08",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 10:01:15",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 10:01:22",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 10:01:30",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 1
    assert alerts[0]["username"] == "bob"
    assert alerts[0]["event_count"] == 5


def test_normal_file_access_not_detected():

    logs = pd.DataFrame([
        {
            "timestamp": "2026-09-27 10:01:01",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 10:01:08",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 10:01:15",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 10:01:22",
            "user": "bob",
            "source_ip": "10.0.0.55",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = detect(logs)

    assert len(alerts) == 0