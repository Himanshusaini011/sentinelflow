import pandas as pd

from src.detection.engine import run_detection_engine


def test_detection_engine_runs_all_rules():

    logs = pd.DataFrame([
        # -----------------------------
        # Brute-force activity
        # -----------------------------
        {
            "timestamp": "2026-09-27 10:01:01",
            "user": "alice",
            "source_ip": "10.0.0.10",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:05",
            "user": "alice",
            "source_ip": "10.0.0.10",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:09",
            "user": "alice",
            "source_ip": "10.0.0.10",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:13",
            "user": "alice",
            "source_ip": "10.0.0.10",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 10:01:17",
            "user": "alice",
            "source_ip": "10.0.0.10",
            "event_type": "LOGIN",
            "status": "FAILED"
        },

        # -----------------------------
        # Failed -> Success activity
        # -----------------------------
        {
            "timestamp": "2026-09-27 11:01:01",
            "user": "bob",
            "source_ip": "10.0.0.20",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 11:01:05",
            "user": "bob",
            "source_ip": "10.0.0.20",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 11:01:09",
            "user": "bob",
            "source_ip": "10.0.0.20",
            "event_type": "LOGIN",
            "status": "FAILED"
        },
        {
            "timestamp": "2026-09-27 11:02:00",
            "user": "bob",
            "source_ip": "10.0.0.20",
            "event_type": "LOGIN",
            "status": "SUCCESS"
        },

        # -----------------------------
        # Suspicious file access
        # -----------------------------
        {
            "timestamp": "2026-09-27 12:01:01",
            "user": "charlie",
            "source_ip": "10.0.0.30",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 12:01:08",
            "user": "charlie",
            "source_ip": "10.0.0.30",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 12:01:15",
            "user": "charlie",
            "source_ip": "10.0.0.30",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 12:01:22",
            "user": "charlie",
            "source_ip": "10.0.0.30",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        },
        {
            "timestamp": "2026-09-27 12:01:30",
            "user": "charlie",
            "source_ip": "10.0.0.30",
            "event_type": "FILE_ACCESS",
            "status": "SUCCESS"
        }
    ])

    logs["timestamp"] = pd.to_datetime(logs["timestamp"])

    alerts = run_detection_engine(logs)

    assert len(alerts) == 3

    reasons = [alert["reason"] for alert in alerts]

    assert any(
        "failed login attempts within 1 minute" in reason
        for reason in reasons
    )

    assert any(
        "followed by successful login" in reason
        for reason in reasons
    )

    assert any(
        "file access within 1 minute" in reason
        for reason in reasons
    )