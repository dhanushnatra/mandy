from data import suppliers, raw_materials,inventory_items, production_batches, purchase_orders
# from models import PurchaseOrderStatus ,Shift

from langchain.tools import tool,BaseTool

from enum import Enum

class Field(Enum):
    SUPPLIER="supplier"
    RAW_MATERIAL="raw_material"
    PRODUCTION_BATCH="production_batch"
    PURCHASE_ORDER="purchase_order"

@tool
def len_of_field(field: Field):
    """Get the count of items in a specific field .
    Args:
        field (Field): The field to get the count for ( supplier, raw_material, production_batch, purchase_order ).
    Returns:
        int or None: The count of items in the specified field, or None if the field is invalid.
    """
    match field:
        case Field.SUPPLIER:
            count = len(suppliers)
        case Field.RAW_MATERIAL:
            count = len(raw_materials)
        case Field.PRODUCTION_BATCH:
            count = len(production_batches)
        case Field.PURCHASE_ORDER:
            count = len(purchase_orders)
        case _:
            print("Invalid field:", field)
            return None
    return f"Total {field.value.replace('_', ' ').title()}s: {count} are present in the database."


@tool
def get_all_suppliers():
    """Retrieve list of all suppliers with name , id , location , material supplied, monthly volume, and rating.
    Returns:
        list[dict]: A list of all suppliers 
                    (
                        supplier_id: str
                        name: str
                        location: str
                        material_supplied: str
                        monthly_volume: int
                        rating: float.
                    )
    """
    print("Retrieving all suppliers")
    return suppliers

@tool
def get_all_raw_materials():
    """Retrieve all raw materials with material_id, name, unit, stock_quantity, reorder_level, and supplier_id.
    Returns:
        list[dict]: A list of all raw materials
        (
            material_id: str
            name: str
            unit: str
            stock_quantity: int
            reorder_level: int
            supplier_id: str
        )
    """
    print("Retrieving all raw materials")
    return f"There are total {len(raw_materials)} raw materials in the database.{"".join([str(material)+"," for material in raw_materials])}", 
@tool
def get_all_production_batches():
    """Retrieve all production batches with batch_id, product_id, quantity, start_date, end_date, and status.
    Returns:
        list[dict]: A list of all production batches.
        (
            batch_id: str
            product: str
            material_used: list[str]
            quantity_produced: int
            date: str
            shift: Shift ( "MORNING", "EVENING", "NIGHT")
        )
        
    """ 
    print("Retrieving all production batches")
    return f"There are total {len(production_batches)} production batches in the database.{"".join([str(batch)+"," for batch in production_batches])}", 
@tool
def get_all_inventory_items():
    """Retrieve all inventory items with inventory_id, name, quantity, location, and status.
    Returns:
        list[dict]: A list of all inventory items.
        (
            inventory_id: str
            product: str
            quantity_available: int
            warehouse: str
            last_updated: str
        )
        
    """
    print("Retrieving all inventory items")
    return f"There are total {len(inventory_items)} inventory items in the database.{"".join([str(item)+"," for item in inventory_items])}", 

@tool
def get_all_purchase_orders():
    """Retrieve all purchase orders with po_id, supplier_id, material_id, quantity, date, and status.
    Returns:
        list[dict]: A list of all purchase orders.
        (
            po_id: str
            supplier_id: str
            material_id: str
            quantity: int
            date: str
            status: PurchaseOrderStatus ( "PENDING", "DELIVERED")
        )
    """
    print("Retrieving all purchase orders")
    return f"There are total {len(purchase_orders)} purchase orders in the database.{"".join([str(order)+"," for order in purchase_orders])}", 

def _get_inventory_item_by_id(inventory_id: str):
    """
    Retrieve an inventory item by its ID.
    Args:
        inventory_id (str): The ID of the inventory item.
    Returns:
        dict or None: The inventory item with the given ID, or None if not found.
    """
    for item in inventory_items:
        if item["inventory_id"] == inventory_id:
            print("Inventory Item Found:", item)
            return item
    return None 

@tool
def get_inventory_item_by_id(inventory_id: str):
    """Retrieve an inventory item by its ID.
    Args:
        inventory_id (str): The ID of the inventory item.
    Returns:
        dict or None: The inventory item with the given ID, or None if not found.
    """
    return _get_inventory_item_by_id(inventory_id)




def _get_supplier_by_id(supplier_id: str):
    """
    Retrieve a supplier by its ID.
    Args:
        supplier_id (str): The ID of the supplier.
    Returns:
        dict or None: The supplier with the given ID, or None if not found.
    """
    for supplier in suppliers:
        if supplier["supplier_id"] == supplier_id:
            print("Supplier Found:", supplier)
            return supplier
    return None

@tool
def get_supplier_by_id(supplier_id: str):
    """Retrieve a supplier by its ID.
    Args:
        supplier_id (str): The ID of the supplier.
    Returns:
        dict or None: The supplier with the given ID, or None if not found.
    """
    return _get_supplier_by_id(supplier_id)

def _get_raw_material_by_id(material_id: str):
    """
    Retrieve a raw material by its ID.
    Args:
        material_id (str): The ID of the raw material.
    Returns:
        dict or None: The raw material with the given ID, or None if not found.
    """
    for material in raw_materials:
        if material["material_id"] == material_id:
            print("Raw Material Found:", material)  
            return material
    return None

@tool
def get_raw_material_by_id(material_id: str):
    """Retrieve a raw material by its ID.
    Args:
        material_id (str): The ID of the raw material.
    Returns:
        dict or None: The raw material with the given ID, or None if not found."""
    return _get_raw_material_by_id(material_id)

def _get_purchase_order_by_id(po_id: str):
    """
    Retrieve a purchase order by its ID.
    Args:
        po_id (str): The ID of the purchase order.
    Returns:
        dict or None: The purchase order with the given ID, or None if not found.
    """
    for order in purchase_orders:
        if order["po_id"] == po_id:
            print("Purchase Order Found:", order)
            return order
    return None


@tool
def get_purchase_order_by_id(po_id: str):
    """Retrieve a purchase order by its ID.
    Args:
        po_id (str): The ID of the purchase order.
    Returns:
        dict or None: The purchase order with the given ID, or None if not found.
    """
    return _get_purchase_order_by_id(po_id)

def _get_production_batch_by_id(batch_id: str):
    """
    Retrieve a production batch by its ID.
    Args:
        batch_id (str): The ID of the production batch.
    Returns:
        dict or None: The production batch with the given ID, or None if not found.
    """

    for batch in production_batches:
        if batch["batch_id"] == batch_id:
            print("Production Batch Found:", batch)
            return batch
    return None

@tool
def get_production_batch_by_id(batch_id: str):
    """Retrieve a production batch by its ID.
    Args:
        batch_id (str): The ID of the production batch.
    Returns:
        dict or None: The production batch with the given ID, or None if not found.
    """
    return _get_production_batch_by_id(batch_id)




@tool
def get_supplier_by_material_name(material_name: str):
    """Retrieve the supplier of a specific raw material by material name.
    Args:
        material_name (str): The name of the raw material.
    Returns:
        dict or None: The supplier of the specified raw material, or None if not found.
    """
    for material in raw_materials:
        if material["name"].lower() == material_name.lower():
            supplier_id = material.get("supplier_id")
            if supplier_id:
                return _get_supplier_by_id(supplier_id)
    return None


@tool
def get_material_by_name(material_name: str):
    """Retrieve a raw material by its name.
    Args:
        material_name (str): The name of the raw material.
    Returns:
        dict or None: The raw material with the given name, or None if not found.
    """
    for material in raw_materials:
        if material["name"].lower() == material_name.lower():
            print("Raw Material Found:", material)
            return material
    return None



@tool
def get_supplier_of_material(material_id: str):
    """Retrieve the supplier of a specific raw material by material ID.
    Args:
        material_id (str): The ID of the raw material.
    Returns:
        dict or None: The supplier of the specified raw material, or None if not found.
    """
    material = _get_raw_material_by_id(material_id)
    if material:
        supplier_id = material.get("supplier_id")
        if supplier_id:
            return _get_supplier_by_id(supplier_id)
    return None

@tool
def get_supplier_from_purchase_order(po_id: str):
    """Retrieve the supplier associated with a specific purchase order by PO ID.
    Args:
        po_id (str): The ID of the purchase order.
    Returns:
        dict or None: The supplier associated with the specified purchase order, or None if not found.
    """
    order = _get_purchase_order_by_id(po_id)
    if order:
        supplier_id = order.get("supplier_id")
        if supplier_id:
            return _get_supplier_by_id(supplier_id)
    return None

@tool
def get_material_from_purchase_order(po_id: str):
    """Retrieve the raw material associated with a specific purchase order by PO ID.
    Args:
        po_id (str): The ID of the purchase order.
    Returns:
        dict or None: The raw material associated with the specified purchase order, or None if not found.
    """
    order = _get_purchase_order_by_id(po_id)
    if order:
        material_id = order["material_id"]
        if material_id:
            return _get_raw_material_by_id(material_id)
    return None

@tool
def get_materials_used_in_production_batch(batch_id: str):
    """Retrieve the raw materials used in a specific production batch by batch ID.
    Args:
        batch_id (str): The ID of the production batch.
    Returns:
        list[dict] or None: A list of raw materials used in the specified production batch, or None if not found.
    """
    batch = _get_production_batch_by_id(batch_id)
    if batch:
        material_ids = batch.get("material_used", [])
        materials = []
        for material_id in material_ids:
            material = _get_raw_material_by_id(material_id)
            if material:
                materials.append(material)
        return materials
    return None

@tool
def get_all_delivered_purchase_orders():
    """Retrieve all delivered purchase orders.
    Returns:
        list[dict]: A list of all delivered purchase orders.
    """
    delivered_orders = [order for order in purchase_orders if order["status"] == "delivered"]
    print("Retrieving all delivered purchase orders")
    return delivered_orders

@tool
def get_all_pending_purchase_orders():
    """Retrieve all pending purchase orders.
    Returns:
        list[dict]: A list of all pending purchase orders.
    """
    pending_orders = [order for order in purchase_orders if order["status"] == "pending"]
    print("Retrieving all pending purchase orders")
    return pending_orders

@tool
def get_low_stock_raw_materials():
    """Retrieve all raw materials that are below their reorder level.
    Returns:
        list[dict]: A list of raw materials that are below their reorder level.
    """
    low_stock_materials = [material for material in raw_materials if material["stock_quantity"] < material["reorder_level"]]
    print("Retrieving all low stock raw materials")
    return low_stock_materials

@tool 
def get_purchase_orders_from_date_to_date(start_date: str, end_date: str):
    """Retrieve all purchase orders within a specific date range.
    Args:
        start_date (str): The start date of the range (inclusive).
        end_date (str): The end date of the range (inclusive).
    Returns:
        list[dict]: A list of purchase orders within the specified date range.
    """
    orders_in_range = [order for order in purchase_orders if start_date <= order["date"] <= end_date]
    print(f"Retrieving all purchase orders from {start_date} to {end_date}")
    return orders_in_range

@tool
def get_production_batches_by_shift(shift: str):
    """Retrieve all production batches for a specific shift.
    Args:
        shift (str): The shift to filter by (e.g., "MORNING", "EVENING", "NIGHT").
    Returns:
        list[dict]: A list of production batches for the specified shift.
    """
    batches_in_shift = [batch for batch in production_batches if batch["shift"] == shift.lower()]
    print(f"Retrieving all production batches for {shift} shift")
    return batches_in_shift

@tool
def get_suppliers_by_rating(min_rating: float):
    """Retrieve all suppliers with a rating above a certain threshold.
    Args:
        min_rating (float): The minimum rating threshold.
    Returns:
        list[dict]: A list of suppliers with a rating above the specified threshold.
    """
    top_suppliers = [supplier for supplier in suppliers if supplier["rating"] >= min_rating]
    print(f"Retrieving all suppliers with rating above {min_rating}")
    return top_suppliers


@tool
def get_inventory_by_product(product_name: str):
    """Retrieve inventory items by product name.
    Args:
        product_name (str): The name of the product to search for.
    Returns:
        list[dict]: A list of inventory items matching the specified product name.
    """
    matching_items = [item for item in inventory_items if item["product"].lower() == product_name.lower()]
    print(f"Retrieving inventory items for product: {product_name}")
    return matching_items

@tool
def get_all_products_in_inventory():
    """Retrieve a list of all unique products in the inventory.
    Returns:
        list[str]: A list of unique product names in the inventory.
    """
    products = set(item["product"] for item in inventory_items)
    print("Retrieving all unique products in inventory")
    return list(products)

@tool
def get_all_products_in_production_batches():
    """Retrieve a list of all unique products in the production batches.
    Returns:
        list[str]: A list of unique product names in the production batches.
    """
    products = set(batch["product"] for batch in production_batches)
    print("Retrieving all unique products in production batches")
    return list(products)

@tool
def get_all_suppliers_locations():
    """Retrieve a list of all unique supplier locations.
    Returns:
        list[str]: A list of unique supplier locations.
    """
    locations = set(supplier["location"] for supplier in suppliers)
    print("Retrieving all unique supplier locations")
    return list(locations)


@tool
def get_all_batches_of_today():
    """Retrieve all production batches created today.
    Returns:
        list[dict]: A list of all production batches created today.
    """
    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")
    todays_batches = [batch for batch in production_batches if batch["date"] == today_str]
    print("Retrieving all production batches created today")
    return todays_batches

@tool
def get_all_low_stock_materials(threshold: int):
    """Retrieve all raw materials with stock quantity below a specified threshold.
    Args:
        threshold (int): The stock quantity threshold.
    Returns:
        list[dict]: A list of raw materials with stock quantity below the specified threshold.
    """
    low_stock_materials = [material for material in raw_materials if material["stock_quantity"] < threshold]
    print(f"Retrieving all raw materials with stock quantity below {threshold}")
    return low_stock_materials        

@tool
def get_batches_this_month():
    """Retrieve all production batches created in the current month.
    Returns:
        list[dict]: A list of all production batches created in the current month.
    """
    from datetime import datetime
    now = datetime.now()
    month_str = now.strftime("%Y-%m")
    monthly_batches = [batch for batch in production_batches if batch["date"].startswith(month_str)]
    print("Retrieving all production batches created this month")
    return monthly_batches

@tool
def get_product_by_warehouse(warehouse_name: str):
    """Retrieve all products stored in a specific warehouse.
    Args:
        warehouse_name (str): The name of the warehouse.
    Returns:
        list[dict]: A list of inventory items stored in the specified warehouse.
    """
    items_in_warehouse = [item for item in inventory_items if item["warehouse"].lower() == warehouse_name.lower()]
    print(f"Retrieving all products in warehouse: {warehouse_name}")
    return items_in_warehouse

@tool
def get_sort_suppliers_by_monthly_volume():
    """Retrieve all suppliers sorted by their monthly volume in descending order.
    Returns:
        list[dict]: A list of suppliers sorted by monthly volume.
    """
    sorted_suppliers = sorted(suppliers, key=lambda x: x["monthly_volume"], reverse=True)
    print("Retrieving all suppliers sorted by monthly volume")
    return sorted_suppliers



all_tools:list[BaseTool] = [
    len_of_field,
    get_all_suppliers,
    get_all_raw_materials,
    get_all_production_batches,
    get_all_purchase_orders,
    get_all_inventory_items,
    get_supplier_of_material,
    get_material_by_name,
    get_supplier_by_id,
    get_raw_material_by_id,
    get_purchase_order_by_id,
    get_production_batch_by_id,
    get_inventory_item_by_id,
    get_supplier_from_purchase_order,
    get_material_from_purchase_order,
    get_materials_used_in_production_batch,
    get_all_delivered_purchase_orders,
    get_all_pending_purchase_orders,
    get_low_stock_raw_materials,
    get_purchase_orders_from_date_to_date,
    get_production_batches_by_shift,
    get_suppliers_by_rating,
    get_inventory_by_product,
    get_all_products_in_inventory,
    get_all_products_in_production_batches,
    get_all_suppliers_locations,
    get_all_batches_of_today,
    get_all_low_stock_materials,
    get_batches_this_month,
    get_product_by_warehouse,
    get_sort_suppliers_by_monthly_volume,
]