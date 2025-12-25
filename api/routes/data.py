from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from core.models import CryptoAsset
from schemas.crypto import CryptoAssetResponse

router = APIRouter(prefix="/data", tags=["Data"])


@router.get("", response_model=List[CryptoAssetResponse])
def get_crypto_data(
    source: Optional[str] = Query(None),
    symbol: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("rank"),
    order: str = Query("asc"),
    db: Session = Depends(get_db),
):
    query = db.query(CryptoAsset)

    # Filtering
    if source:
        query = query.filter(CryptoAsset.source == source)

    if symbol:
        query = query.filter(CryptoAsset.symbol.ilike(symbol.upper()))

    # Sorting
    sort_column = getattr(CryptoAsset, sort_by, None)
    if sort_column is not None:
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    # Pagination
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    return results
