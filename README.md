# Kasparro Backend & ETL System

This repository contains a **production-grade backend and ETL system** built as part of the **Kasparro Backend & ETL Systems Assignment**.

The project demonstrates **end-to-end ownership** of a backend system, including:
- Data ingestion from multiple sources
- Incremental ETL with checkpointing and recovery
- Normalized relational schema
- API layer with pagination, filtering, and metadata
- Dockerized, runnable system
- Automated tests
- Clean, scalable architecture

---

##  What This Project Does

This system ingests cryptocurrency market data from **multiple sources**, processes it through an **ETL pipeline**, stores it in **PostgreSQL**, and exposes the data through a **FastAPI backend**.

### High-level capabilities:
- Ingest raw data from:
   CoinPaprika API
   CoinGecko API
   CSV data source
- Store raw data in `raw_*` tables
- Normalize data into a unified `crypto_assets` schema
- Perform **incremental ingestion** (no duplicate processing)
- Track ETL progress using checkpoints
- Recover safely from failures
- Expose APIs for querying data and ETL statistics
- Run fully via Docker

---

##  Architecture Overview
<img width="1024" height="1487" alt="ChatGPT Image Dec 26, 2025, 03_43_50 AM" src="https://github.com/user-attachments/assets/ee486dc2-7c97-4b0e-bf4f-9c2d9f41759a" />

---

##  Project Structure
<img width="452" height="817" alt="image" src="https://github.com/user-attachments/assets/22076f14-1608-4008-b6a9-e00a6902fe35" />

---

##  ETL Design & Incremental Ingestion

### Raw Tables
Each data source stores raw payloads without modification:
- `raw_coinpaprika`
- `raw_coingecko`
- `raw_csv`

This allows:
- Reprocessing if schemas change
- Debugging source-level issues
- Safe recovery from failures

### Normalized Table
All sources are unified into:
- `crypto_assets`

This table provides a clean, queryable schema for APIs.

### Checkpointing
The `etl_checkpoint` table tracks:
- Source name
- Last processed timestamp
- Success & failure timestamps
- Running status

This enables:
- Resume-on-failure
- Idempotent writes
- No duplicate processing

---

##  API Endpoints

### `GET /health`
Checks system health.

**Returns:**
- API status
- Database connectivity
- API latency
- Unique request ID

---

### `GET /data`
Returns normalized crypto asset data.

**Features:**
- Pagination (`limit`, `offset`)
- Filtering (symbol, source)
- Sorting (price, market cap, rank)

---

### `GET /stats`
Returns ETL run statistics.

**Includes:**
- Records processed
- Last success timestamp
- Last failure timestamp
- ETL run metadata

---

##  Running the Project (Docker)

### Prerequisites
- Docker
- Docker Compose

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/HrishithaBathula/kasparro-backend-hrishitha-bathula.git
cd kasparro-backend-hrishitha-bathula
```
### Step 2: Configure Environment Variables

Create a .env file:
```bash
COINPAPRIKA_API_KEY=your_api_key_here
```
### Step 3: Build & Run
```bash
docker compose up --build
```

This will:

Start PostgreSQL

Run ETL ingestion automatically

Start the FastAPI server

### Step 4: Access the API
```bash
API Base URL: http://localhost:8000

Health Check: http://localhost:8000/health

Data API: http://localhost:8000/data

Stats API: http://localhost:8000/stats
```

## Running Tests

Locally (inside virtual environment)
```bash
pytest -v
```
---
## Covered Scenarios

1) API endpoint correctness

2) ETL model existence

3) Failure handling

4) Database connectivity failure simulation
---
## Docker Commands 

If make is available:

**make up**

**make down**

**make test**


Otherwise:

**docker compose up --build**

**docker compose down**

---

## Security Considerations

1) API keys are loaded via environment variables

2) No secrets are hard-coded

---

### This project was built to reflect real-world backend engineering standards, focusing on:

**1) Reliability**

**2) Observability**

**3) Maintainability**

**4) Clear separation of concerns**


**The system is ready to be extended, deployed to cloud infrastructure, and scheduled for periodic ETL runs.**

---

**Author: Hrishitha Bathula**

**Assignment: Kasparro Backend & ETL Systems**
