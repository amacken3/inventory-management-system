class InventoryService:
    def __init__(self, inventory):
        self._inventory = inventory
    
    def get_all_items(self):
        return self._inventory
    
    def get_item_by_id(self, item_id):
        for item in self._inventory:
            if item["id"] == item_id:
                return item