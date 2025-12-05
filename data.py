import json
from models import Supplier, RawMaterial, ProductionBatch, PurchaseOrder, InventoryItem

def load_data():
    with open('./dataset.json', 'r') as file:
        data = json.load(file)
    return data

data: dict = load_data()

suppliers = [Supplier(**item) for item in data.get('suppliers', [])]
raw_materials = [RawMaterial(**item) for item in data.get('raw_materials', [])]
production_batches = [ProductionBatch(**item) for item in data.get('production_batches', [])]
purchase_orders = [PurchaseOrder(**item) for item in data.get('purchase_orders', [])]
inventory_items = [InventoryItem(**item) for item in data.get('inventory_items', [])]