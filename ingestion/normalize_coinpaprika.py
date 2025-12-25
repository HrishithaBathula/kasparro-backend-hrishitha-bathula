from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.models import RawCoinPaprika, CryptoAsset


def normalize_coinpaprika():
    print("Starting CoinPaprika normalization...")

    db: Session = SessionLocal()

    try:
        raw_rows = db.query(RawCoinPaprika).all()
        print(f"Found {len(raw_rows)} raw records")

        for row in raw_rows:
            data = row.payload

            usd = data.get("quotes", {}).get("USD", {})

            asset = CryptoAsset(
                source="coinpaprika",
                asset_id=data.get("id"),
                symbol=data.get("symbol"),
                name=data.get("name"),
                rank=data.get("rank"),
                price_usd=usd.get("price"),
                market_cap_usd=usd.get("market_cap"),
                volume_24h_usd=usd.get("volume_24h"),
            )

            db.add(asset)

        db.commit()
        print("Normalization completed successfully.")

    except Exception as e:
        db.rollback()
        print("Normalization failed:", e)

    finally:
        db.close()
        
if __name__ == "__main__":
    normalize_coinpaprika()
