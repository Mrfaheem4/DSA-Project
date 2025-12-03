# Quick Start Guide - TechStore

## ⚡ Get Running in 2 Minutes

### Step 1: Install Dependencies
```powershell
cd ecommerce_platform\backend
pip install -r requirements.txt
```

### Step 2: Start Flask Backend
```powershell
python app.py
```
You should see:
```
WARNING in flask.app.create_app_from_factory: Warning: The default charset for json has changed from 'utf-8' to 'utf-8-sig'.
Running on http://127.0.0.1:5000
```

### Step 3: Open Frontend
In another PowerShell window:
```powershell
cd ecommerce_platform\frontend
python -m http.server 8000
```

Then open your browser:
- **Frontend**: http://localhost:8000
- **API**: http://localhost:5000/api

## 🧪 Test the Application

### Test Products API
```powershell
# In PowerShell or visit in browser
curl http://localhost:5000/api/products
curl http://localhost:5000/api/health
```

### Test Shopping Flow
1. Open http://localhost:8000 in browser
2. Browse products
3. Click "Add to Cart" on any product
4. Click cart icon (🛍️) to view
5. Click "Proceed to Checkout"
6. View order in "View Orders" button

## 📊 DSA Usage in Application

| Feature | DSA Used | Time Complexity |
|---------|----------|-----------------|
| Product Lookup | Binary Search Tree | O(log n) |
| Stock Check | Hash Table | O(1) |
| Add to Cart | Queue | O(1) |
| Order History | LinkedList | O(n) |
| Recent Orders | Stack | O(1) |

## 🔌 API Response Examples

### Get All Products
```
GET http://localhost:5000/api/products
Response: [
  {
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "stock": 10,
    "category": "Electronics",
    "description": "High-performance laptop"
  },
  ...
]
```

### Add to Cart
```
POST http://localhost:5000/api/cart/user_123/add
Body: {"product_id": 1, "quantity": 1}
Response: {"message": "Product added to cart", "cart": [...]}
```

### Checkout
```
POST http://localhost:5000/api/checkout
Body: {"user_id": "user_123"}
Response: {
  "message": "Order placed successfully",
  "order": {
    "order_id": 1,
    "user_id": "user_123",
    "items": [...],
    "total": 999.99,
    "status": "confirmed"
  }
}
```

## 🎨 UI Features

- **Product Grid**: Responsive card layout with emoji icons
- **Real-time Search**: Filter products as you type
- **Category Filter**: Quick filtering by Electronics, Accessories, Audio
- **Shopping Cart**: Slide-out sidebar with cart items
- **Order History**: View all recent orders with details
- **Notifications**: Toast notifications for actions
- **Mobile Responsive**: Works on phones, tablets, and desktops

## 🔧 Customize

### Change Product Emoji
Edit `frontend/js/app.js`:
```javascript
const productEmojis = {
    'Laptop': '💻',
    'Mouse': '🖱️',
    // Add more...
};
```

### Change Colors
Edit `frontend/css/styles.css`:
```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    /* ... */
}
```

### Add New Products
Edit `backend/app.py`:
```python
SAMPLE_PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10, ...},
    {"id": 7, "name": "Your Product", "price": 99.99, "stock": 20, ...},  # Add here
]
```

## ❌ Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | `netstat -ano \| findstr :5000` then kill the process |
| ModuleNotFoundError: flask | Run `pip install -r requirements.txt` |
| CORS error | Make sure Flask server is running on port 5000 |
| Cannot find localhost:8000 | Make sure you're in frontend folder and ran http.server |

## 📚 Understanding the Code

### Backend Flow
```
Request → Flask Route → DSA Structure (BST/Hash/Queue/etc) → Response
```

### Frontend Flow
```
User Action → JavaScript Event → Fetch API Call → Update UI
```

### Cart Process (Using Queue - FIFO)
```
Add Item → enqueue() → Remove Item → dequeue() (first added is first removed)
```

### Order Process
```
Checkout → Store in LinkedList (all orders) → Store in Stack (recent) → Clear Cart
```

## 🚀 Next Steps

1. Add user authentication (login/signup)
2. Implement payment processing (Stripe/PayPal)
3. Add product reviews and ratings
4. Implement wishlist (using another DSA like Set)
5. Add admin dashboard for inventory management
6. Database integration (MongoDB/PostgreSQL)
7. Deployment (Heroku/AWS/Azure)

---

**Enjoy your e-commerce platform!** 🎉
