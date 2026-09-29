import pandas as pd


def load_security_logs(file_path):
    """
    Load security logs from a CSV file.
    """

    logs = pd.read_csv(file_path)

    # Preserve original CSV row number
    logs["source_row_number"] = range(2, len(logs) + 2)

    return logs