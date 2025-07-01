import pytest
from gpt_service import GPTRecommendationService
import asyncio


@pytest.mark.asyncio
async def test_parse_gpt_response():
    service = GPTRecommendationService()
    response = "1, 2, 3"
    ids = service._parse_gpt_response(response)
    assert ids == [1, 2, 3]


@pytest.mark.asyncio
async def test_find_products_by_ids():
    service = GPTRecommendationService()
    products = [
        {"id": 1, "name": "A"},
        {"id": 2, "name": "B"},
        {"id": 3, "name": "C"},
    ]
    ids = [2, 3]
    result = service._find_products_by_ids(ids, products)
    assert len(result) == 2
    assert result[0]["id"] == 2
    assert result[1]["id"] == 3
