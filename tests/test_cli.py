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