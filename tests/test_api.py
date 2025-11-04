import pytest
import os
import sys
from fastapi.testclient import TestClient

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from main import app


class TestAPI:
    """Тесты для API endpoints"""

    def test_root_endpoint(self, client: TestClient):
        """Тест корневой страницы"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Home Page"}

    def test_get_user_endpoint(self, client: TestClient):
        """Тест endpoint /get_user"""
        response = client.get("/get_user")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_get_user_with_valid_id(self, client: TestClient):
        """Тест endpoint /get_user/{user_id} с валидным ID"""
        user_id = 123
        response = client.get(f"/get_user/{user_id}")
        assert response.status_code == 200
        assert response.json() == {"user_id": user_id}

    def test_get_user_with_different_ids(self, client: TestClient):
        """Тест с разными ID пользователей"""
        test_ids = [1, 42, 1000, 999999]
        for user_id in test_ids:
            response = client.get(f"/get_user/{user_id}")
            assert response.status_code == 200
            assert response.json() == {"user_id": user_id}

    # Исправленный параметризованный тест
    @pytest.mark.parametrize("user_id,expected_status,should_contain_user_id", [
        (1, 200, True),
        (42, 200, True),
        (0, 400, False),
        (-1, 400, False),
    ])
    def test_get_user_parameterized(self, client: TestClient, user_id, expected_status, should_contain_user_id):
        """Параметризованный тест для разных ID"""
        response = client.get(f"/get_user/{user_id}")
        assert response.status_code == expected_status

        if should_contain_user_id:
            assert response.json()["user_id"] == user_id
        else:
            assert "user_id" not in response.json()


class TestAPIEdgeCases:
    """Тесты для граничных случаев"""

    def test_invalid_user_id_string(self, client: TestClient):
        """Тест с невалидным строковым ID"""
        response = client.get("/get_user/abc")
        assert response.status_code == 422  # Validation error

    def test_nonexistent_endpoint(self, client: TestClient):
        """Тест несуществующего endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_method_not_allowed(self, client: TestClient):
        """Тест неподдерживаемого HTTP метода"""
        response = client.post("/get_user/123")
        assert response.status_code == 405
