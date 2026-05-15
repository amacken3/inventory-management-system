from unittest.mock import patch
from services.openfoodfacts_service import OpenFoodFactsService


def test_get_product_by_barcode_returns_clean_product_data():
    service = OpenFoodFactsService()

    mock_response_data = {
        "code": "3017624010701",
        "status": 1,
        "status_verbose": "product found",
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "sugar, palm oil, hazelnuts",
            "nutrition_grades": "e"
        }
    }

    with patch("services.openfoodfacts_service.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        product = service.get_product_by_barcode("3017624010701")

    assert product == {
        "name": "Nutella",
        "brand": "Ferrero",
        "barcode": "3017624010701",
        "ingredients": "sugar, palm oil, hazelnuts",
        "nutrition_grade": "e"
    }


def test_get_product_by_barcode_returns_none_when_product_not_found():
    service = OpenFoodFactsService()

    mock_response_data = {
        "code": "0000000000000",
        "status": 0,
        "status_verbose": "product not found"
    }

    with patch("services.openfoodfacts_service.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        product = service.get_product_by_barcode("0000000000000")

    assert product is None


def test_get_product_by_barcode_returns_none_when_api_fails():
    service = OpenFoodFactsService()

    with patch("services.openfoodfacts_service.requests.get") as mock_get:
        mock_get.return_value.status_code = 500

        product = service.get_product_by_barcode("3017624010701")

    assert product is None

