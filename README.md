# SentinelFlow

## Security Data Engineering & Threat Detection Platform

SentinelFlow is a Python and PostgreSQL-based security data pipeline that ingests security logs, validates and transforms events, stores them in PostgreSQL, and applies rule-based threat detection to identify suspicious activity.

The project is designed as an evolving Data Engineering + Cybersecurity platform, starting with batch processing and PostgreSQL and providing a foundation for future streaming, distributed processing, and cloud deployment.

---

## Architecture

```text
                    Security Logs
                         │
                         ▼
                  ┌─────────────┐
                  │  Ingestion  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │Transformation│
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Validation  │
                  └──────┬──────┘
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
          Valid Events       Invalid Events
                │                 │
                ▼                 ▼
          PostgreSQL         Quarantine
                │
                ▼
        Threat Detection Engine
                │
        ┌───────┼────────┬──────────────┐
        ▼       ▼        ▼              ▼
    Brute     Failed →  File         Suspicious
    Force     Success   Access       IP Activity
        │       │        │              │
        └───────┴────────┴──────────────┘
                         │
                         ▼
                  Security Alerts
                         │
                         ▼
                     PostgreSQL
```

---

## Key Features

* CSV-based security log ingestion
* Pandas-based data transformation
* Data validation and invalid-record quarantine
* PostgreSQL event storage
* Batch-level ingestion tracking
* Duplicate event protection
* Rule-based threat detection
* PostgreSQL security alert storage
* Duplicate alert protection
* Structured application logging
* Automated unit tests with pytest

---

## Threat Detection Rules

### 1. Brute Force Detection

Detects multiple failed login attempts from the same IP address.

**Condition:**

* Event type: `LOGIN`
* Status: `FAILED`
* At least 5 attempts
* Within 1 minute
* Same source IP

Example:

```text
10.0.0.55
FAILED
FAILED
FAILED
FAILED
FAILED
```

Result:

```text
Security Alert
Reason: Multiple failed login attempts within 1 minute
```

---

### 2. Failed Login → Successful Login

Detects a successful login occurring after multiple failed login attempts from the same user and IP.

**Condition:**

* Same username
* Same source IP
* At least 3 failed attempts
* Failed attempts occur within 5 minutes before success

This can help identify login activity where repeated failures are followed by a successful authentication.

---

### 3. Suspicious File Access

Detects unusually frequent file-access events from the same user.

**Condition:**

* Event type: `FILE_ACCESS`
* At least 5 events
* Within 1 minute
* Same user

---

### 4. Suspicious IP Activity

Detects an IP address generating failed login attempts against multiple users.

**Condition:**

* Event type: `LOGIN`
* Status: `FAILED`
* At least 3 failed attempts
* Within 1 minute
* At least 3 different users
* Same source IP

This helps identify activity where one IP is targeting multiple accounts.

---

## Data Pipeline

SentinelFlow processes security events through the following stages:

### 1. Ingestion

Reads security events from:

```text
data/raw/security_logs.csv
```

### 2. Transformation

Normalizes the incoming data and prepares it for validation and processing.

### 3. Validation

Checks incoming records for data-quality issues.

Valid records continue through the pipeline.

Invalid records are sent to the quarantine system instead of being inserted into the main event table.

### 4. PostgreSQL Loading

Valid security events are stored in the:

```text
security_events
```

table.

The system uses source-file and source-row information to prevent the same source record from being inserted repeatedly.

### 5. Threat Detection

The detection engine runs all registered security rules against the validated dataset.

### 6. Alert Storage

Detected alerts are stored in:

```text
security_alerts
```

Duplicate alerts are ignored using PostgreSQL conflict handling.

### 7. Ingestion Tracking

Every pipeline execution is tracked using:

```text
ingestion_runs
```

The pipeline records:

* Batch ID
* Source file
* Start time
* Completion time
* Records received
* Records loaded
* Records quarantined
* Pipeline status

Possible execution states include:

```text
RUNNING
SUCCESS
FAILED
```

---

## Database

SentinelFlow currently uses PostgreSQL.

### Main Tables

| Table                       | Purpose                          |
| --------------------------- | -------------------------------- |
| `security_events`           | Stores validated security events |
| `security_event_quarantine` | Stores invalid records           |
| `security_alerts`           | Stores detected security alerts  |
| `ingestion_runs`            | Tracks pipeline executions       |

### Data Integrity

The pipeline uses PostgreSQL constraints and conflict handling to prevent duplicate source records and duplicate security alerts.

---

## Project Structure

```text
sentinelflow/
│
├── data/
│   └── raw/
│       └── security_logs.csv
│
├── logs/
│   └── sentinelflow.log
│
├── main.py
│
├── src/
│   ├── database/
│   │   ├── alerts.py
│   │   ├── connection.py
│   │   ├── ingestion_runs.py
│   │   ├── loader.py
│   │   └── quarantine.py
│   │
│   ├── detection/
│   │   ├── engine.py
│   │   └── rules/
│   │       ├── brute_force.py
│   │       ├── failed_then_success.py
│   │       ├── suspicious_file_access.py
│   │       └── suspicious_ip_activity.py
│   │
│   ├── ingestion/
│   │   └── load_data.py
│   │
│   ├── transformation/
│   │   └── transform_data.py
│   │
│   ├── validation/
│   │   └── validate_data.py
│   │
│   └── utils/
│       └── logger.py
│
└── tests/
    ├── test_brute_force.py
    ├── test_detection_engine.py
    ├── test_failed_then_success.py
    ├── test_suspicious_file_access.py
    └── test_suspicious_ip_activity.py
```

---

## Technologies

* **Python**
* **Pandas**
* **PostgreSQL**
* **psycopg**
* **pytest**
* **UUID**
* **Python logging**

---

## Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd sentinelflow
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```text
sentinelflow
```

Configure the database password through:

```bash
export SENTINELFLOW_DB_PASSWORD="your_password"
```

The application connects using:

```text
Host: localhost
Port: 5432
Database: sentinelflow
User: postgres
```

### 5. Run tests

```bash
pytest -q
```

### 6. Run SentinelFlow

```bash
python3 main.py
```

---

## Example Output

```text
================================
      SENTINELFLOW
================================

[1] Loading security logs...
Loaded 15 records.

[2] Transforming data...
Data transformation completed.

[3] Validating data...
Valid records: 14
Quarantined records: 1

[4] Processing data quality issues...
Quarantined: 0

[5] Loading valid records...
Inserted into database: 0

[6] Running threat detection...

================================
       SECURITY RESULTS
================================

🚨 SECURITY ALERT
Source IP: 10.0.0.55
Event Count: 5
Start Time: 2026-09-12 10:01:11
End Time: 2026-09-12 10:01:23
Reason: Multiple failed login attempts within 1 minute
```

---

## Testing

SentinelFlow includes automated tests for the detection system.

Current test coverage includes:

* Brute-force detection
* Failed-login-to-success detection
* Suspicious file-access detection
* Suspicious IP activity detection
* Detection engine integration

Run:

```bash
pytest -q
```

Current project status:

```text
9 tests passed
```

---

## Current Scope

The current version is a batch-oriented security data engineering platform using CSV input, Python/Pandas processing, PostgreSQL storage, and rule-based detection.

The architecture is intentionally designed so that additional components can be introduced without replacing the existing pipeline.

---

## Future Development

Planned evolution of SentinelFlow:

```text
Current
CSV
 ↓
Python/Pandas
 ↓
PostgreSQL
 ↓
Rule-Based Detection
```

Future:

```text
Multiple Security Log Sources
          ↓
       Airflow
          ↓
        Kafka
          ↓
       PySpark
          ↓
     Data Lake
          ↓
Threat Detection
          ↓
     Dashboard
          ↓
        Cloud
```

Potential future technologies include:

* Apache Airflow
* Apache Kafka
* Apache Spark / PySpark
* Cloud object storage
* Cloud databases
* Real-time streaming
* Security monitoring dashboards
* Distributed processing
* Containerized deployment

---

## Project Goal

SentinelFlow is being developed as a practical project combining **Data Engineering and Cybersecurity**.

The goal is to build an increasingly scalable platform capable of handling security data from ingestion through processing, storage, analysis, and threat detection.
