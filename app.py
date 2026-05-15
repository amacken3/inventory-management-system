from flask import Flask, jsonify
from data.inventory_data import inventory
from services.inventory_service import InventoryService

app = Flask(__name__)

inventory_service = InventoryService(inventory)

@app.route("/")
def home():
    return jsonify({"message": "Inventory Management API"})

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory_service.get_all_items()), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = inventory_service.get_item_by_id(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)