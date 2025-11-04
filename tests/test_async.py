import pytest
import os
import sys
from httpx import AsyncClient, ASGITransport

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from main import app

@pytest.mark.asyncio
async def test_async_root():
    """Асинхронный тест"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Home Page"}