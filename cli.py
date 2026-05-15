import requests

BASE_URL = "http://127.0.0.1:5555"

def print_item(item, show_ingredients=False):
    print(f"ID: {item['id']}")
    print(f"Name: {item['name']}")
    print(f"Brand: {item['brand']}")
    print(f"Barcode: {item['barcode']}")
    print(f"Price: ${item['price']}")
    print(f"Stock: {item['stock']}")
    print(f"Nutrition Grade: {item.get('nutrition_grade', 'N/A')}")

    if show_ingredients:
        print(f"Ingredients: {item.get('ingredients', 'N/A')}")

    print("-" * 30)

def list_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code != 200:
        print("Failed to fetch inventory.")
        return

    inventory = response.json()

    if not inventory:
        print("Inventory is empty.")
        return

    for item in inventory:
        print_item(item)

def get_inventory_item(item_id):
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        item = response.json()
        print_item(item, show_ingredients=True)

    elif response.status_code == 404:
        error = response.json()
        print(error["error"])

    else:
        print("Failed to fetch item.")

def search_product(barcode):
    response = requests.get(f"{BASE_URL}/inventory/search/{barcode}")

    if response.status_code == 200:
        product = response.json()
        print(f"Name: {product['name']}")
        print(f"Brand: {product['brand']}")
        print(f"Barcode: {product['barcode']}")
        print(f"Nutrition Grade: {product.get('nutrition_grade', 'N/A')}")
        print(f"Ingredients: {product.get('ingredients', 'N/A')}")
    
    elif response.status_code == 404:
        error = response.json()
        print(error["error"])

    else:
        print("Failed to search product")

def import_product(barcode, price, stock):
    response = requests.post(
        f"{BASE_URL}/inventory/import/{barcode}",
        json={"price": price, "stock": stock}
    )

    if response.status_code == 201:
        item = response.json()
        print("Product imported successfully!")
        print_item(item, show_ingredients=True)

    elif response.status_code in [400, 404]:
        error = response.json()
        print(error["error"])

    else:
        print("Failed to import product.")