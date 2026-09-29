from src.detection.rules import brute_force
from src.detection.rules import failed_then_success
from src.detection.rules import suspicious_file_access


def run_detection_engine(logs):
    """
    Run all registered security detection rules.
    """

    alerts = []

    rules = [
        brute_force.detect,
        failed_then_success.detect,
        suspicious_file_access.detect
    ]

    for rule in rules:

        rule_alerts = rule(logs)

        alerts.extend(rule_alerts)

    return alerts