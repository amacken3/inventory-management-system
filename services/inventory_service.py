class InventoryService:
    def __init__(self, inventory):
        self._inventory = inventory
    
    def get_all_items(self):
        return self._inventory
    
    def get_item_by_id(self, item_id):
        for item in self._inventory:
            if item["id"] == item_id:
                return item
            
        return None
    
    def create_item(self, data):
        highest_id = 0

        for item in self._inventory:
            if item["id"] > highest_id:
                highest_id = item["id"]

        new_item = {
            "id": highest_id + 1,
            "name": data["name"],
            "brand": data["brand"],
            "barcode": data["barcode"],
            "price": data["price"],
            "stock": data["stock"],
            "ingredients": data.get("ingredients", ""),
            "nutrition_grade": data.get("nutrition_grade", "")
        }

        self._inventory.append(new_item)

        return new_item
    
    def update_item(self, item_id, data):
        for item in self._inventory:
            if item["id"] == item_id:
                for key, value in data.items():
                    if key != "id":
                        item[key] = value
                    
                return item
            
        return None
    
    def delete_item(self, item_id):
        for item in self._inventory:
            if item["id"] == item_id:
                self._inventory.remove(item)
                return item
        
        return None