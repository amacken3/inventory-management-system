import requests

class OpenFoodFactsService:
    def __init__(self):
        self._base_url = "https://world.openfoodfacts.org/api/v2/product"
        self._headers = {
            "User-Agent": "InventoryManagementSystem/1.0 (aengus.2000@gmail.com)"
        }

    def get_product_by_barcode(self, barcode):
        url = f"{self._base_url}/{barcode}.json"

        response = requests.get(url, headers=self._headers)

        if response.status_code != 200:
            return None
        
        data = response.json()

        if data.get("status") != 1:
            return None
        
        product = data.get("product", {})

        return {
            "name": product.get("product_name", ""),
            "brand": product.get("brands", ""),
            "barcode": data.get("code", barcode),
            "ingredients": product.get("ingredients_text", ""),
            "nutrition_grade": product.get("nutrition_grades", "")
        }