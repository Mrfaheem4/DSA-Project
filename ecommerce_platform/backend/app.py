from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
from models.dsa import (
    LinkedList, Queue, BinarySearchTree, InventoryArray, Stack
)

app = Flask(__name__)
CORS(app)

# Initialize DSA structures
products_bst = BinarySearchTree()
inventory_array = InventoryArray()
orders_history = LinkedList()
user_carts = {}  # Dictionary to store carts for each user
order_history_stack = Stack()

# Sample products database
SAMPLE_PRODUCTS = [
    # Gaming Category
    {"id": 1, "name": "Gaming Laptop", "price": 1299.99, "stock": 8, "category": "Gaming", "description": "High-performance gaming laptop with RTX 4060", "image": "images/gaming_laptop.jpg"},
    {"id": 2, "name": "Gaming Mouse", "price": 59.99, "stock": 40, "category": "Gaming", "description": "RGB gaming mouse with 16000 DPI", "image": "images/gaming_mouse.jpeg"},
    {"id": 3, "name": "Gaming Keyboard", "price": 129.99, "stock": 25, "category": "Gaming", "description": "Mechanical gaming keyboard with RGB lighting", "image": "images/gaming_keyboard.jpg"},
    {"id": 4, "name": "Gaming Headset", "price": 199.99, "stock": 20, "category": "Gaming", "description": "7.1 surround sound gaming headset", "image": "images/gaming_headset.jpeg"},
    {"id": 5, "name": "Gaming Monitor", "price": 399.99, "stock": 12, "category": "Gaming", "description": "27-inch 144Hz gaming monitor", "image": "images/gaming_monitor.jpeg"},
    
    # Office Work Category
    {"id": 6, "name": "Office Laptop", "price": 799.99, "stock": 15, "category": "Office Work", "description": "Lightweight laptop for office productivity", "image": "images/office_laptop.jpg"},
    {"id": 7, "name": "Wireless Mouse", "price": 29.99, "stock": 50, "category": "Office Work", "description": "Ergonomic wireless mouse", "image": "images/wireless_mouse.jpeg"},
    {"id": 8, "name": "Office Keyboard", "price": 79.99, "stock": 35, "category": "Office Work", "description": "Quiet mechanical keyboard for office", "image": "images/office_keyboard.jpeg"},
    {"id": 9, "name": "USB-C Hub", "price": 49.99, "stock": 45, "category": "Office Work", "description": "7-in-1 USB-C hub for connectivity", "image": "images/usbc_hub.jpg"},
    {"id": 10, "name": "Desk Lamp", "price": 39.99, "stock": 30, "category": "Office Work", "description": "LED desk lamp with adjustable brightness", "image": "images/desk_lamp.jpg"},
    
    # Appliances Category
    {"id": 11, "name": "Smart Speaker", "price": 99.99, "stock": 25, "category": "Appliances", "description": "Voice-controlled smart speaker", "image": "images/smart_speaker.jpg"},
    {"id": 12, "name": "Portable Charger", "price": 44.99, "stock": 60, "category": "Appliances", "description": "20000mAh power bank with fast charging", "image": "images/portable_charger.jpeg"},
    {"id": 13, "name": "USB-C Charger", "price": 34.99, "stock": 55, "category": "Appliances", "description": "65W fast charging USB-C adapter", "image": "images/usbc_charger.jpg"},
    {"id": 14, "name": "Wireless Charger", "price": 24.99, "stock": 50, "category": "Appliances", "description": "15W Qi wireless charging pad", "image": "images/wireless_charger.jpg"},
    {"id": 15, "name": "Smart Thermostat", "price": 249.99, "stock": 10, "category": "Appliances", "description": "WiFi-enabled smart thermostat", "image": "images/smart_thermostat.jpeg"},
    
    # Accessories Category
    {"id": 16, "name": "Phone Stand", "price": 19.99, "stock": 70, "category": "Accessories", "description": "Adjustable phone stand for desk", "image": "images/phone_stand.jpg"},
    {"id": 17, "name": "Cable Organizer", "price": 14.99, "stock": 80, "category": "Accessories", "description": "Cable management organizer kit", "image": "images/cable_organizer.jpeg"},
    {"id": 18, "name": "Screen Protector Pack", "price": 9.99, "stock": 100, "category": "Accessories", "description": "Pack of 3 tempered glass screen protectors", "image": "images/screen_protector.jpeg"},
    {"id": 19, "name": "HDMI Cable", "price": 12.99, "stock": 90, "category": "Accessories", "description": "2m HDMI 2.1 cable", "image": "images/hdmi_cable.jpeg"},
    {"id": 20, "name": "USB-A to USB-C", "price": 8.99, "stock": 120, "category": "Accessories", "description": "USB-A to USB-C adapter cable", "image": "images/usb_adapter.jpg"},
    
    # Lights Category
    {"id": 21, "name": "RGB LED Strip", "price": 29.99, "stock": 40, "category": "Lights", "description": "5m RGB LED strip with remote control", "image": "images/rgb_ledstrip.jpg"},
    {"id": 22, "name": "Smart Bulb", "price": 19.99, "stock": 55, "category": "Lights", "description": "WiFi-enabled smart LED bulb", "image": "images/smart_bulb.jpeg"},
    {"id": 23, "name": "Desk Ring Light", "price": 69.99, "stock": 20, "category": "Lights", "description": "10-inch ring light for streaming", "image": "images/ring_light.jpg"},
    {"id": 24, "name": "Ambient Light", "price": 39.99, "stock": 35, "category": "Lights", "description": "Smart ambient lighting system", "image": "images/ambient_light.jpeg"},
    {"id": 25, "name": "Neon Sign", "price": 79.99, "stock": 15, "category": "Lights", "description": "Customizable neon LED sign", "image": "images/neon_sign.jpg"},
]

# Initialize system
def initialize_system():
    """Initialize products and inventory"""
    for product in SAMPLE_PRODUCTS:
        products_bst.insert(product["id"], product)
        inventory_array.insert(product["id"], product["stock"])

initialize_system()

# Routes

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with updated inventory"""
    products = products_bst.inorder_traversal()
    # Update stock from inventory_array
    for product in products:
        stock = inventory_array.search(product["id"])
        if stock is not None:
            product["stock"] = stock
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    product = products_bst.search(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Get all inventory levels"""
    return jsonify(inventory_array.get_all())

@app.route('/api/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    """Get user's shopping cart"""
    if user_id not in user_carts:
        user_carts[user_id] = Queue()
    
    cart_items = user_carts[user_id].get_items()
    
    # Calculate total and item count
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return jsonify({
        "items": cart_items,
        "total": round(total, 2),
        "item_count": len(cart_items)
    })

@app.route('/api/cart/<user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    """Add product to cart using Queue (FIFO)"""
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Get product from BST
    product = products_bst.search(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    # Check inventory
    stock = inventory_array.search(product_id)
    if stock is None or stock < quantity:
        return jsonify({"error": "Insufficient inventory"}), 400
    
    # Initialize cart if needed
    if user_id not in user_carts:
        user_carts[user_id] = Queue()
    
    # Add to cart (enqueue)
    cart_item = {
        "id": product_id,
        "name": product["name"],
        "price": product["price"],
        "quantity": quantity,
        "category": product["category"]
    }
    user_carts[user_id].enqueue(cart_item)
    
    return jsonify({
        "message": "Product added to cart",
        "cart": user_carts[user_id].get_items()
    })

@app.route('/api/cart/<user_id>/remove', methods=['POST'])
def remove_from_cart(user_id):
    """Remove product from cart using Queue (DEQUEUE - removes first item)"""
    if user_id not in user_carts:
        return jsonify({"error": "Cart not found"}), 404
    
    removed = user_carts[user_id].dequeue()
    if removed is None:
        return jsonify({"error": "Cart is empty"}), 400
    
    return jsonify({
        "message": "Product removed from cart",
        "removed": removed,
        "cart": user_carts[user_id].get_items()
    })

@app.route('/api/cart/<user_id>/clear', methods=['POST'])
def clear_cart(user_id):
    """Clear entire cart"""
    if user_id not in user_carts:
        user_carts[user_id] = Queue()
    
    user_carts[user_id].clear()
    return jsonify({"message": "Cart cleared"})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process checkout"""
    data = request.json
    user_id = data.get('user_id')
    
    if user_id not in user_carts or user_carts[user_id].is_empty():
        return jsonify({"error": "Cart is empty"}), 400
    
    cart_items = user_carts[user_id].get_items()
    
    # Verify inventory and deduct
    for item in cart_items:
        stock = inventory_array.search(item['id'])
        if stock is None or stock < item['quantity']:
            return jsonify({"error": f"Insufficient inventory for {item['name']}"}), 400
    
    # Process order - deduct inventory
    order_total = 0
    for item in cart_items:
        current_stock = inventory_array.search(item['id'])
        new_stock = current_stock - item['quantity']
        inventory_array.insert(item['id'], new_stock)
        order_total += item['price'] * item['quantity']
    
    # Create order using LinkedList (orders_history)
    order = {
        "order_id": len(orders_history.to_list()) + 1,
        "user_id": user_id,
        "items": cart_items,
        "total": round(order_total, 2),
        "timestamp": datetime.now().isoformat(),
        "status": "confirmed"
    }
    
    # Store in LinkedList
    orders_history.append(order)
    
    # Store in Stack for recent orders
    order_history_stack.push(order)
    
    # Clear user cart
    user_carts[user_id].clear()
    
    return jsonify({
        "message": "Order placed successfully",
        "order": order
    })

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders from LinkedList"""
    orders = orders_history.to_list()
    return jsonify(orders)

@app.route('/api/recent-orders', methods=['GET'])
def get_recent_orders():
    """Get recent orders from Stack (LIFO)"""
    recent = order_history_stack.get_items()
    return jsonify(recent)

@app.route('/api/search', methods=['GET'])
def search_products():
    """Search products by query"""
    query = request.args.get('q', '').lower()
    products = products_bst.inorder_traversal()
    
    results = [p for p in products if 
               query in p['name'].lower() or 
               query in p['description'].lower()]
    
    return jsonify(results)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "products": len(products_bst.inorder_traversal()),
        "orders": len(orders_history.to_list())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
