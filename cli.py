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