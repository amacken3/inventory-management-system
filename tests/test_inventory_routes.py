import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
    
def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Inventory Management API"}

def test_get_inventory_returns_list(client):
    response = client.get("/inventory")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_inventory_item_by_id(client):
    response = client.get("/inventory/1")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["id"] == 1
    assert "name" in data

def test_get_inventory_item_returns_404_for_missing_item(client):
    response = client.get("/inventory/999")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Item not found"