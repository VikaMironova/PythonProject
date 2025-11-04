import pytest
import os, sys
from fastapi.testclient import TestClient

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from main import app

@pytest.fixture
def client():
    """Фикстура для тестового клиента"""
    with TestClient(app) as test_client:
        yield test_client

def test_root(client):
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Home Page"}