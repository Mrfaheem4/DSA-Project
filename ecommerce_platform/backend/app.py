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

# Load products from external file (products.txt)
PRODUCTS_FILE = 'products.txt'

TECH_KEYWORDS = [
    'laptop', 'mouse', 'keyboard', 'monitor', 'headset', 'webcam', 'speaker',
    'charger', 'usb', 'hdmi', 'thermostat', 'camera', 'power bank'
]

TECH_CATEGORIES = ['gaming', 'office work', 'appliances', 'lights']

def load_products_from_file():
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            products = json.load(f)
            return products
    except Exception:
        return []


# Initialize system using products loaded from products.txt
def initialize_system():
    products = load_products_from_file()
    for product in products:
        # Normalize category and name checks
        name = product.get('name', '').lower()
        cat = product.get('category', '').lower()

        # If product matches tech keywords or belongs to a tech category, move to 'Tech'
        if any(k in name for k in TECH_KEYWORDS) or (cat in TECH_CATEGORIES):
            product['category'] = 'Tech'

        products_bst.insert(product['id'], product)
        inventory_array.insert(product['id'], product.get('stock', 0))

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
