import pytest
from database import ProductDatabase
import asyncio


@pytest.mark.asyncio
async def test_load_products():
    db = ProductDatabase()
    products = await db.load_products(limit=2)
    assert isinstance(products, list)
    if products:
        assert isinstance(products[0], dict)
        assert len(products[0]) > 0
