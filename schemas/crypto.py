from pydantic import BaseModel
from typing import Optional


class CryptoAssetResponse(BaseModel):
    source: str
    asset_id: str
    symbol: Optional[str]
    name: Optional[str]
    rank: Optional[int]
    price_usd: Optional[float]
    market_cap_usd: Optional[float]
    volume_24h_usd: Optional[float]

    class Config:
        from_attributes = True
