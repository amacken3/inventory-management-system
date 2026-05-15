import requests

BASE_URL = "http://127.0.0.1:5555"

def list_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code != 200:
        print("Failed to fetch inventory.")
        return

    inventory = response.json()

    for item in inventory:
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Brand: {item['brand']}")
        print(f"Price: ${item['price']}")
        print(f"Stock: {item['stock']}")
        print("-" * 20)