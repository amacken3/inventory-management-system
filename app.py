from flask import Flask, jsonify, request
from data.inventory_data import inventory
from services.inventory_service import InventoryService
from services.openfoodfacts_service import OpenFoodFactsService

app = Flask(__name__)

inventory_service = InventoryService(inventory)

openfoodfacts_service = OpenFoodFactsService()

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

@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json()

    required_fields = ["name", "brand", "barcode", "price", "stock"]

    for field in required_fields:
        if not data or field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_item = inventory_service.create_item(data)

    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    updated_item = inventory_service.update_item(item_id, data)

    if updated_item is None:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify(updated_item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    deleted_item = inventory_service.delete_item(item_id)

    if deleted_item is None:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify({"message": "Item deleted successfully"}), 200

@app.route("/inventory/search/<barcode>", methods=["GET"])
def search_inventory_by_barcode(barcode):
    product = openfoodfacts_service.get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200

@app.route("/inventory/import/<barcode>", methods=["POST"])
def import_product_by_barcode(barcode):
    data = request.get_json()

    required_fields = ["price", "stock"]

    for field in required_fields:
        if not data or field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    product = openfoodfacts_service.get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    product["price"] = data["price"]
    product["stock"] = data["stock"]

    new_item = inventory_service.create_item(product)

    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)