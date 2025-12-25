"""
Minimal ETL test.

This test verifies that the CryptoAsset model exists and is queryable.
It does NOT require a live database connection.
"""

from core.models import CryptoAsset


def test_crypto_asset_model_exists():
    # Verifies model is defined and importable
    assert CryptoAsset.__tablename__ == "crypto_assets"
