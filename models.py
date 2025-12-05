from typing import TypedDict
from enum import Enum


class Shift(Enum):
    MORNING = "morning"
    EVENING = "evening"
    NIGHT = "night"
    
class PurchaseOrderStatus(Enum):
    PENDING="pending"
    DELIVERED="delivered"

class Supplier(TypedDict):
    supplier_id: str
    name: str
    location: str
    material_supplied: str
    monthly_volume: int
    rating: float
    
class RawMaterial(TypedDict):
    material_id: str
    name: str
    unit: str
    stock_quantity: int
    reorder_level: int
    supplier_id: str
    
class ProductionBatch(TypedDict):
    batch_id: str
    product: str
    material_used: list[str]
    quantity_produced: int
    date: str
    shift: Shift


class PurchaseOrder(TypedDict):
    po_id: str
    supplier_id: str
    material_id: str
    quantity: int
    date: str
    status: PurchaseOrderStatus

class InventoryItem(TypedDict):
    inventory_id: str
    product: str
    quantity_available: int
    warehouse: str
    last_updated: str