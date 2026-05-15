import pytest
from app import app
from unittest.mock import patch


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

def test_create_inventory_item(client):
    new_item = {
        "name": "Peanut Butter",
        "brand": "Jif",
        "barcode": "123456789012",
        "price": 3.99,
        "stock": 20,
        "ingredients": "Peanuts, sugar, salt",
        "nutrition_grade": "c"
    }

    response = client.post("/inventory", json=new_item)
    data = response.get_json()

    assert response.status_code == 201
    assert isinstance(data, dict)
    assert "id" in data
    assert data["name"] == "Peanut Butter"
    assert data["brand"] == "Jif"
    assert data["barcode"] == "123456789012"
    assert data["price"] == 3.99
    assert data["stock"] == 20

def test_create_inventory_item_requires_name(client):
    new_item = {
        "brand": "Jif",
        "barcode": "123456789012",
        "price": 3.99,
        "stock": 20
    }

    response = client.post("/inventory", json=new_item)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Missing required field: name"

def test_update_inventory_item(client):
    updated_data = {
        "stock": 30,
        "price": 4.49
    }

    response = client.patch("/inventory/1", json=updated_data)
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["stock"] == 30
    assert data["price"] == 4.49


def test_update_inventory_item_returns_404_for_missing_item(client):
    updated_data = {
        "stock": 30
    }

    response = client.patch("/inventory/999", json=updated_data)
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Item not found"

def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Item deleted successfully"


def test_delete_inventory_item_returns_404_for_missing_item(client):
    response = client.delete("/inventory/999")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Item not found"

def test_search_inventory_by_barcode_returns_product_data(client):
    mock_product = {
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "ingredients": "sugar, palm oil, hazelnuts",
        "nutrition_grade": "e"
    }

    with patch("app.openfoodfacts_service.get_product_by_barcode") as mock_get_product:
        mock_get_product.return_value = mock_product

        response = client.get("/inventory/search/3017624010701")
        data = response.get_json()

    assert response.status_code == 200
    assert data == mock_product
    mock_get_product.assert_called_once_with("3017624010701")


def test_search_inventory_by_barcode_returns_404_when_product_not_found(client):
    with patch("app.openfoodfacts_service.get_product_by_barcode") as mock_get_product:
        mock_get_product.return_value = None

        response = client.get("/inventory/search/0000000000000")
        data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Product not found"

def test_import_product_by_barcode_adds_product_to_inventory(client):
    mock_product = {
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "ingredients": "sugar, palm oil, hazelnuts",
        "nutrition_grade": "e"
    }

    request_data = {
        "price": 5.99,
        "stock": 12
    }

    with patch("app.openfoodfacts_service.get_product_by_barcode") as mock_get_product:
        mock_get_product.return_value = mock_product

        response = client.post("/inventory/import/3017624010701", json=request_data)
        data = response.get_json()

    assert response.status_code == 201
    assert "id" in data
    assert data["name"] == "Nutella"
    assert data["brand"] == "Ferrero"
    assert data["barcode"] == "3017624010701"
    assert data["ingredients"] == "sugar, palm oil, hazelnuts"
    assert data["nutrition_grade"] == "e"
    assert data["price"] == 5.99
    assert data["stock"] == 12

    mock_get_product.assert_called_once_with("3017624010701")


def test_import_product_by_barcode_requires_price(client):
    request_data = {
        "stock": 12
    }

    response = client.post("/inventory/import/3017624010701", json=request_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Missing required field: price"


def test_import_product_by_barcode_requires_stock(client):
    request_data = {
        "price": 5.99
    }

    response = client.post("/inventory/import/3017624010701", json=request_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Missing required field: stock"


def test_import_product_by_barcode_returns_404_when_product_not_found(client):
    request_data = {
        "price": 5.99,
        "stock": 12
    }

    with patch("app.openfoodfacts_service.get_product_by_barcode") as mock_get_product:
        mock_get_product.return_value = None

        response = client.post("/inventory/import/0000000000000", json=request_data)
        data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Product not found"