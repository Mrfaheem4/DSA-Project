# TechStore - E-commerce Platform

A full-stack e-commerce application built with **Python (Flask)** backend featuring **DSA implementations**, and a modern **JavaScript/CSS/HTML** frontend.

## 🎯 Features

### Data Structures & Algorithms Implemented
- **Binary Search Tree (BST)**: Efficient product lookup by ID - O(log n) search time
- **Hash Table**: Fast inventory management with O(1) average lookup
- **Queue (FIFO)**: Shopping cart implementation for managing items in order
- **LinkedList**: Order history storage with O(n) sequential access
- **Stack (LIFO)**: Recent orders tracking for quick access
- **Linked List Traversal**: Dynamic order retrieval and management

### E-commerce Features
✅ Product browsing with filtering by category
✅ Real-time search functionality
✅ Shopping cart with add/remove items
✅ Inventory management with stock validation
✅ Order checkout with inventory deduction
✅ Order history tracking
✅ Responsive design for mobile & desktop
✅ RESTful API architecture

## 📁 Project Structure

```
ecommerce_platform/
├── backend/
│   ├── models/
│   │   └── dsa.py              # DSA implementations
│   ├── app.py                  # Flask application & API routes
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── index.html              # Main HTML file
│   ├── css/
│   │   └── styles.css          # Responsive styling
│   └── js/
│       └── app.js              # Frontend logic & API calls
└── README.md                   # This file
```

## 🚀 Installation & Setup

### Backend Setup

1. **Install Python Dependencies**
   ```powershell
   cd ecommerce_platform\backend
   pip install -r requirements.txt
   ```

2. **Run Flask Server**
   ```powershell
   python app.py
   ```
   - Server will run at `http://localhost:5000`
   - API endpoints are available at `http://localhost:5000/api`

### Frontend Setup

1. **Open in Browser**
   - Navigate to `frontend/index.html` in your web browser
   - Or use a local web server:
   ```powershell
   # Using Python 3
   cd ecommerce_platform\frontend
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

## 📡 API Endpoints

### Products
- **GET** `/api/products` - Get all products
- **GET** `/api/products/<id>` - Get product by ID
- **GET** `/api/search?q=query` - Search products

### Shopping Cart
- **GET** `/api/cart/<user_id>` - Get user's cart
- **POST** `/api/cart/<user_id>/add` - Add item to cart
- **POST** `/api/cart/<user_id>/remove` - Remove item from cart
- **POST** `/api/cart/<user_id>/clear` - Clear entire cart

### Orders
- **POST** `/api/checkout` - Process checkout
- **GET** `/api/orders` - Get all orders (LinkedList)
- **GET** `/api/recent-orders` - Get recent orders (Stack)

### Inventory
- **GET** `/api/inventory` - Get all inventory levels

## 💻 Technology Stack

### Backend
- **Python 3.x**
- **Flask** - Web framework
- **Flask-CORS** - Cross-Origin Resource Sharing

### Frontend
- **HTML5** - Markup
- **CSS3** - Responsive styling with Flexbox & Grid
- **Vanilla JavaScript** - No dependencies, pure JS
- **Fetch API** - AJAX requests to backend

## 📊 DSA Implementations

### 1. Binary Search Tree (Products)
- **Purpose**: Efficient product lookup by ID
- **Time Complexity**: O(log n) for search
- **Location**: `models/dsa.py` - `BinarySearchTree` class
- **Usage**: Product retrieval in O(log n) time

### 2. Hash Table (Inventory)
- **Purpose**: Fast stock level management
- **Time Complexity**: O(1) average lookup
- **Location**: `models/dsa.py` - `HashTable` class
- **Usage**: Instant inventory checks during checkout

### 3. Queue (Shopping Cart)
- **Purpose**: FIFO ordering of cart items
- **Time Complexity**: O(1) enqueue/dequeue
- **Location**: `models/dsa.py` - `Queue` class
- **Usage**: Managing cart with proper item ordering

### 4. LinkedList (Order History)
- **Purpose**: Sequential order storage and traversal
- **Time Complexity**: O(n) traversal
- **Location**: `models/dsa.py` - `LinkedList` class
- **Usage**: Complete order history with dynamic growth

### 5. Stack (Recent Orders)
- **Purpose**: LIFO access to most recent orders
- **Time Complexity**: O(1) push/pop
- **Location**: `models/dsa.py` - `Stack` class
- **Usage**: Quick access to recent transactions

## 🎮 How to Use

1. **View Products**: Browse the product listing with product details
2. **Search**: Use the search bar to find products by name or description
3. **Filter**: Use category filters to narrow down products
4. **Add to Cart**: Click "Add to Cart" to add items
5. **View Cart**: Click the cart icon to see items
6. **Checkout**: Click "Proceed to Checkout" to complete purchase
7. **View Orders**: Click "View Orders" in footer to see order history

## 🔍 Sample Data

The system comes with 6 sample products:
- Laptop ($999.99)
- Mouse ($29.99)
- Keyboard ($79.99)
- Monitor ($299.99)
- Headphones ($149.99)
- Webcam ($89.99)

## 📱 Responsive Design

- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (320px - 767px)

## 🛠️ Development Notes

### Adding New Products
Edit `app.py` in the `SAMPLE_PRODUCTS` list:
```python
SAMPLE_PRODUCTS = [
    {"id": 1, "name": "Product", "price": 99.99, "stock": 10, "category": "Category", "description": "..."},
    # Add more products
]
```

### Adding Product Categories
Update the filter buttons in `index.html` and add corresponding filter logic in `app.js`.

### Custom Styling
Modify `frontend/css/styles.css` to customize colors and layout:
```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    /* ... other colors ... */
}
```

## 🐛 Troubleshooting

**Issue**: CORS Error
- **Solution**: Ensure Flask server is running with `Flask-CORS` enabled

**Issue**: API not responding
- **Solution**: Check if Flask server is running on `http://localhost:5000`

**Issue**: Products not loading
- **Solution**: Verify the DSA structures are initialized in `app.py`

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Built as a demonstration of Data Structures & Algorithms in Python with a modern web interface.

---

**Happy Shopping!** 🛒💳
