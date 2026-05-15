from unittest.mock import patch
import cli


def test_list_inventory_displays_items(capsys):
    mock_inventory = [
        {
            "id": 1,
            "name": "Nutella",
            "brand": "Ferrero",
            "barcode": "3017624010701",
            "price": 5.99,
            "stock": 10,
            "ingredients": "sugar, palm oil, hazelnuts",
            "nutrition_grade": "e"
        }
    ]

    with patch("cli.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_inventory

        cli.list_inventory()

    captured = capsys.readouterr()

    assert "Nutella" in captured.out
    assert "Ferrero" in captured.out
    assert "Stock: 10" in captured.out

def test_get_inventory_item_displays_item(capsys):
    mock_item = {
        "id": 1,
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "price": 5.99,
        "stock": 10,
        "ingredients": "sugar, palm oil, hazelnuts",
        "nutrition_grade": "e"
    }

    with patch("cli.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_item

        cli.get_inventory_item(1)

    captured = capsys.readouterr()

    assert "Nutella" in captured.out
    assert "Ferrero" in captured.out
    assert "Stock: 10" in captured.out
    assert "Ingredients: sugar, palm oil, hazelnuts" in captured.out


def test_get_inventory_item_displays_error_when_not_found(capsys):
    with patch("cli.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"error": "Item not found"}

        cli.get_inventory_item(999)

    captured = capsys.readouterr()

    assert "Item not found" in captured.out

def test_search_product_displays_product_data(capsys):
    mock_product = {
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "ingredients": "sugar, palm oil, hazelnuts",
        "nutrition_grade": "e"
    }

    with patch("cli.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_product

        cli.search_product("3017624010701")

    captured = capsys.readouterr()

    assert "Nutella" in captured.out
    assert "Ferrero" in captured.out
    assert "3017624010701" in captured.out
    assert "Nutrition Grade: e" in captured.out
    assert "Ingredients: sugar, palm oil, hazelnuts" in captured.out


def test_search_product_displays_error_when_not_found(capsys):
    with patch("cli.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"error": "Product not found"}

        cli.search_product("0000000000000")

    captured = capsys.readouterr()

    assert "Product not found" in captured.out

def test_import_product_displays_created_item(capsys):
    mock_item = {
        "id": 3,
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "price": 5.99,
        "stock": 12,
        "ingredients": "sugar, palm oil, hazelnuts",
        "nutrition_grade": "e"
    }

    with patch("cli.requests.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_item

        cli.import_product("3017624010701", 5.99, 12)

    captured = capsys.readouterr()

    assert "Product imported successfully!" in captured.out
    assert "Nutella" in captured.out
    assert "Ferrero" in captured.out
    assert "Stock: 12" in captured.out
    assert "Ingredients: sugar, palm oil, hazelnuts" in captured.out

    mock_post.assert_called_once_with(
        "http://127.0.0.1:5555/inventory/import/3017624010701",
        json={"price": 5.99, "stock": 12}
    )


def test_import_product_displays_error(capsys):
    with patch("cli.requests.post") as mock_post:
        mock_post.return_value.status_code = 404
        mock_post.return_value.json.return_value = {"error": "Product not found"}

        cli.import_product("0000000000000", 5.99, 12)

    captured = capsys.readouterr()

    assert "Product not found" in captured.out

def test_delete_inventory_item_displays_success_message(capsys):
    with patch("cli.requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {
            "message": "Item deleted successfully"
        }

        cli.delete_inventory_item(1)

    captured = capsys.readouterr()

    assert "Item deleted successfully" in captured.out

    mock_delete.assert_called_once_with(
        "http://127.0.0.1:5555/inventory/1"
    )


def test_delete_inventory_item_displays_error_when_not_found(capsys):
    with patch("cli.requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 404
        mock_delete.return_value.json.return_value = {
            "error": "Item not found"
        }

        cli.delete_inventory_item(999)

    captured = capsys.readouterr()

    assert "Item not found" in captured.out

def test_update_inventory_item_displays_updated_item(capsys):
    mock_item = {
        "id": 1,
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "price": 4.49,
        "stock": 30,
        "ingredients": "sugar, palm oil, hazelnuts",
        "nutrition_grade": "e"
    }

    updates = {
        "price": 4.49,
        "stock": 30
    }

    with patch("cli.requests.patch") as mock_patch:
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = mock_item

        cli.update_inventory_item(1, updates)

    captured = capsys.readouterr()

    assert "Item updated successfully!" in captured.out
    assert "Nutella" in captured.out
    assert "Price: $4.49" in captured.out
    assert "Stock: 30" in captured.out

    mock_patch.assert_called_once_with(
        "http://127.0.0.1:5555/inventory/1",
        json=updates
    )


def test_update_inventory_item_displays_error_when_not_found(capsys):
    updates = {
        "stock": 30
    }

    with patch("cli.requests.patch") as mock_patch:
        mock_patch.return_value.status_code = 404
        mock_patch.return_value.json.return_value = {
            "error": "Item not found"
        }

        cli.update_inventory_item(999, updates)

    captured = capsys.readouterr()

    assert "Item not found" in captured.out