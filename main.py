import uuid

from src.ingestion.load_data import load_security_logs
from src.transformation.transform_data import transform_security_logs
from src.validation.validate_data import validate_security_logs
from src.detection.engine import run_detection_engine
from src.database.loader import load_security_events
from src.database.quarantine import load_quarantined_events
from src.database.ingestion_runs import (
    start_ingestion_run,
    update_records_received,
    complete_ingestion_run
)
from src.database.alerts import save_security_alerts
from src.utils.logger import logger


def main():

    file_path = "data/raw/security_logs.csv"

    ingestion_batch_id = uuid.uuid4()
    source_file = file_path

    inserted_count = 0
    quarantined_count = 0
    run_started = False

    print("================================")
    print("      SENTINELFLOW")
    print("================================")

    logger.info(
        f"Pipeline started | Batch ID: {ingestion_batch_id}"
    )

    try:

        # -----------------------------------
        # START INGESTION RUN
        # -----------------------------------

        start_ingestion_run(
            ingestion_batch_id,
            source_file,
            0
        )

        run_started = True

        # -----------------------------------
        # 1. INGESTION
        # -----------------------------------

        print("\n[1] Loading security logs...")

        logs = load_security_logs(file_path)

        update_records_received(
            ingestion_batch_id,
            len(logs)
        )

        print(f"Loaded {len(logs)} records.")

        logger.info(
            f"Loaded {len(logs)} security records"
        )

        # -----------------------------------
        # 2. TRANSFORMATION
        # -----------------------------------

        print("\n[2] Transforming data...")

        logs = transform_security_logs(logs)

        print("Data transformation completed.")

        logger.info(
            "Data transformation completed"
        )

        # -----------------------------------
        # 3. VALIDATION
        # -----------------------------------

        print("\n[3] Validating data...")

        valid_logs, quarantined_records = (
            validate_security_logs(logs)
        )

        print(
            f"Valid records: {len(valid_logs)}"
        )

        print(
            f"Quarantined records: "
            f"{len(quarantined_records)}"
        )

        # -----------------------------------
        # 4. QUARANTINE
        # -----------------------------------

        print("\n[4] Processing data quality issues...")

        quarantined_count = load_quarantined_events(
            quarantined_records,
            source_file
        )

        print(
            f"Quarantined: {quarantined_count}"
        )

        # -----------------------------------
        # 5. DATABASE LOADING
        # -----------------------------------

        print("\n[5] Loading valid records...")

        if not valid_logs.empty:

            inserted_count = load_security_events(
                valid_logs,
                ingestion_batch_id,
                source_file
            )

        print(
            f"Inserted into database: "
            f"{inserted_count}"
        )

        # -----------------------------------
        # 6. THREAT DETECTION
        # -----------------------------------

        print("\n[6] Running threat detection...")

        alerts = run_detection_engine(
            valid_logs
        )

        logger.info(
            f"Threat detection completed. "
            f"{len(alerts)} alert(s) generated"
        )

        stored_alerts = save_security_alerts(
            alerts
        )

        logger.info(
            f"{stored_alerts} new security alert(s) "
            f"stored in PostgreSQL"
        )

        # -----------------------------------
        # 7. COMPLETE INGESTION RUN
        # -----------------------------------

        complete_ingestion_run(
            ingestion_batch_id,
            inserted_count,
            quarantined_count,
            status="SUCCESS"
        )

        # -----------------------------------
        # 8. SECURITY RESULTS
        # -----------------------------------

        print("\n================================")
        print("       SECURITY RESULTS")
        print("================================")

        if not alerts:

            print(
                "\nNo suspicious activity detected."
            )

        else:

            for alert in alerts:

                print("\n🚨 SECURITY ALERT")

                print(
                    f"Source IP: "
                    f"{alert['source_ip']}"
                )

                if alert.get("username"):

                    print(
                        f"Username: "
                        f"{alert['username']}"
                    )

                print(
                    f"Event Count: "
                    f"{alert['event_count']}"
                )

                print(
                    f"Start Time: "
                    f"{alert['start_time']}"
                )

                print(
                    f"End Time: "
                    f"{alert['end_time']}"
                )

                print(
                    f"Reason: "
                    f"{alert['reason']}"
                )

                logger.warning(
                    f"Suspicious activity detected "
                    f"from {alert['source_ip']}"
                )

        logger.info(
            "Pipeline completed successfully"
        )

    except Exception as error:

        logger.exception(
            f"Pipeline failed: {error}"
        )

        if run_started:

            try:

                complete_ingestion_run(
                    ingestion_batch_id,
                    inserted_count,
                    quarantined_count,
                    status="FAILED"
                )

            except Exception as update_error:

                logger.exception(
                    f"Failed to update ingestion run status: "
                    f"{update_error}"
                )

        raise


if __name__ == "__main__":
    main()

