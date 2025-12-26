import os
import time
import uuid
from core.database import init_db
from fastapi import FastAPI, Depends
from sqlalchemy import text
from core.database import get_db
from ingestion.coinpaprika_ingest import ingest_coinpaprika
from api.routes.data import router as data_router

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


app = FastAPI(title="Kasparro Backend Assignment")
app.include_router(data_router)

@app.get("/")
def root():
    return {
        "service": "Kasparro Backend API",
        "available_endpoints": {
            "health": "/health",
            "data": "/data",
            "stats": "/stats"
        }
    }
    
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

    # Detect Railway public URL
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")

    if railway_domain:
        BASE_URL = f"https://{railway_domain}"
    else:
        BASE_URL = "http://localhost:8000"

    print("\nKasparro API is running!")
    print(f"API Base URL   : {BASE_URL}", flush=True)
    print(f"Health Check  : {BASE_URL}/health", flush=True )
    print(f"Data Endpoint : {BASE_URL}/data", flush=True)
    print(f"Stats Endpoint: {BASE_URL}/stats\n", flush=True)

    init_db()
    ingest_coinpaprika()


   

