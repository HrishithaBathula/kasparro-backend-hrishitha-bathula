from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    Boolean,
    func,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()




class RawCoinPaprika(Base):
    __tablename__ = "raw_coinpaprika"

    id = Column(Integer, primary_key=True)
    source_id = Column(String, index=True)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, server_default=func.now())

class RawCoinGecko(Base):
    __tablename__ = "raw_coingecko"

    id = Column(Integer, primary_key=True)
    source_id = Column(String, index=True)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, server_default=func.now())

class RawCSV(Base):
    __tablename__ = "raw_csv"

    id = Column(Integer, primary_key=True)
    source_id = Column(String, index=True)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(DateTime, server_default=func.now())

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    asset_id = Column(String, nullable=False)
    symbol = Column(String)
    name = Column(String)
    rank = Column(Integer)
    price_usd = Column(Float)
    market_cap_usd = Column(Float)
    volume_24h_usd = Column(Float)
    created_at = Column(DateTime, server_default=func.now())


class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoint"

    id = Column(Integer, primary_key=True)
    source = Column(String, unique=True, nullable=False)
    last_processed_at = Column(DateTime)
    last_success = Column(DateTime)
    last_failure = Column(DateTime)
    is_running = Column(Boolean, default=False)
