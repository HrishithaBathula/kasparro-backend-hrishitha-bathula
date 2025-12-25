import csv
from datetime import datetime
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.models import RawCSV, ETLCheckpoint


CSV_SOURCE_NAME = "csv_source"
CSV_FILE_PATH = "data/crypto_sample.csv"


def ingest_csv():
    print("Starting CSV ingestion...")

    db: Session = SessionLocal()

    try:
        # Check checkpoint
        checkpoint = (
            db.query(ETLCheckpoint)
            .filter(ETLCheckpoint.source == CSV_SOURCE_NAME)
            .first()
        )

        if checkpoint and checkpoint.last_success:
            print("CSV already ingested. Skipping.")
            return

        if not checkpoint:
            checkpoint = ETLCheckpoint(
                source=CSV_SOURCE_NAME,
                is_running=True,
            )
            db.add(checkpoint)
            db.commit()

        with open(CSV_FILE_PATH, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        print(f"Read {len(rows)} rows from CSV")

        for row in rows:
            record = RawCSV(payload=row)
            db.add(record)

        checkpoint.last_success = datetime.utcnow()
        checkpoint.is_running = False

        db.commit()
        print("CSV ingestion completed successfully.")

    except Exception as e:
        db.rollback()
        checkpoint.last_failure = datetime.utcnow()
        checkpoint.is_running = False
        db.commit()
        print("CSV ingestion failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    ingest_csv()
