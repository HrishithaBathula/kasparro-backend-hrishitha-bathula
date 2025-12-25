import time
import uuid
from core.database import init_db
from fastapi import FastAPI, Depends
from sqlalchemy import text
from core.database import get_db
from ingestion.coinpaprika_ingest import ingest_coinpaprika
from api.routes.data import router as data_router


app = FastAPI(title="Kasparro Backend Assignment")
app.include_router(data_router)


@app.get("/health")
def health_check(db=Depends(get_db)):
    start = time.time()
    try:
        db.execute(text("SELECT 1"))
        status = "connected"
    except Exception:
        status = "disconnected"

    latency = int((time.time() - start) * 1000)

    return {
        "status": "ok",
        "db": status,
        "api_latency_ms": latency,
        "request_id": str(uuid.uuid4())
    }

@app.get("/stats")
def etl_stats(db=Depends(get_db)):
    result = db.execute(
        text("""
        SELECT
            source,
            last_processed_at,
            last_success,
            last_failure,
            is_running
        FROM etl_checkpoint
        ORDER BY source
        """)
    ).mappings().all()

    return {
        "status": "ok",
        "etl_sources": result
    }


@app.on_event("startup")
def startup():
    print(">>> Startup triggered")
    init_db()
   

