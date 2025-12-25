import requests
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import SessionLocal
from core.models import RawCoinPaprika, ETLCheckpoint


def ingest_coinpaprika():
    print("Starting CoinPaprika ingestion...")

    db: Session = SessionLocal()

    try:
        # 1️⃣ Always ensure checkpoint row exists
        checkpoint = (
            db.query(ETLCheckpoint)
            .filter(ETLCheckpoint.source == "coinpaprika")
            .first()
        )

        if not checkpoint:
            checkpoint = ETLCheckpoint(
                source="coinpaprika",
                is_running=False
            )
            db.add(checkpoint)
            db.commit()
            print("Checkpoint row created for coinpaprika")

        # 2️⃣ If already succeeded earlier → skip
        if checkpoint.last_success:
            print("CoinPaprika already ingested earlier. Skipping.")
            return

        # 3️⃣ Mark ETL as running
        checkpoint.is_running = True
        db.commit()

        # 4️⃣ Call CoinPaprika API
        url = "https://api.coinpaprika.com/v1/tickers"
        response = requests.get(url)
        data = response.json()

        print(f"Fetched {len(data)} records from CoinPaprika")

        # 5️⃣ Insert raw data
        for coin in data:
            db.add(RawCoinPaprika(payload=coin))

        db.commit()

        # 6️⃣ Mark success
        checkpoint.last_success = datetime.utcnow()
        checkpoint.is_running = False
        db.commit()

        print("CoinPaprika ingestion completed successfully.")

    except Exception as e:
        db.rollback()
        print("Error during CoinPaprika ingestion:", e)

        checkpoint.last_failure = datetime.utcnow()
        checkpoint.is_running = False
        db.commit()

    finally:
        db.close()
