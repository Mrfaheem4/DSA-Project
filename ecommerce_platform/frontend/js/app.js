// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';
const USER_ID = 'user_' + Math.random().toString(36).substr(2, 9);

// Initialize theme
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('themeToggle').textContent = '☀️';
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        document.getElementById('themeToggle').textContent = '🌙';
    }
}

// Toggle theme
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    document.getElementById('themeToggle').textContent = newTheme === 'dark' ? '☀️' : '🌙';
}

// Product Emojis
const productEmojis = {
    'Laptop': '💻',
    'Mouse': '🖱️',
    'Keyboard': '⌨️',
    'Monitor': '🖥️',
    'Headphones': '🎧',
    'Webcam': '📷'
};

// State
let allProducts = [];
let filteredProducts = [];
let currentFilter = 'all';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    loadProducts();
    updateCartUI();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', handleSearch);
}

// Load Products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (!response.ok) throw new Error('Failed to load products');
        
        allProducts = await response.json();
        filteredProducts = allProducts;
        renderProducts(filteredProducts);
        showNotification('Products loaded successfully', 'success');
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Failed to load products', 'error');
    }
}

// Render Products
function renderProducts(products) {
    const productsList = document.getElementById('productsList');
    
    if (products.length === 0) {
        productsList.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #7f8c8d;">No products found</p>';
        return;
    }
    
    productsList.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22200%22%3E%3Crect fill=%22%23ecf0f1%22 width=%22200%22 height=%22200%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 font-size=%2224%22 text-anchor=%22middle%22 dy=%22.3em%22%3E${ '📦'}%3C/text%3E%3C/svg%3E'">
                <div class="product-overlay">
                    <button class="overlay-btn" onclick="addToCart(${product.id}, '${product.name}', ${product.price})" ${product.stock <= 0 ? 'disabled' : ''}>
                        Add to Cart
                    </button>
                    <button class="overlay-btn" onclick="viewProductDetails(${product.id}, '${product.name}')">
                        View Details
                    </button>
                </div>
            </div>
            <div class="product-content">
                <div class="product-name">${product.name}</div>
                <span class="product-category">${product.category}</span>
            </div>
        </div>
    `).join('');
}

// View Product Details
function viewProductDetails(productId, productName) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;
    
    const modal = document.getElementById('productModal');
    document.getElementById('modalProductName').textContent = product.name;
    
    const detailsHTML = `
        <div style="text-align: center; margin: 20px 0;">
            <img src="${product.image}" alt="${product.name}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22300%22 height=%22300%22%3E%3Crect fill=%22%23ecf0f1%22 width=%22300%22 height=%22300%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 font-size=%2240%22 text-anchor=%22middle%22 dy=%22.3em%22%3E${productEmojis[product.name] || '📦'}%3C/text%3E%3C/svg%3E'">
        </div>
        <h3>Price</h3>
        <p style="font-size: 24px; color: #27ae60; font-weight: bold;">$${product.price.toFixed(2)}</p>
        
        <h3>Category</h3>
        <p>${product.category}</p>
        
        <h3>Description</h3>
        <p>${product.description}</p>
        
        <h3>Availability</h3>
        <p>${product.stock > 0 ? `✅ In Stock (${product.stock} units available)` : '❌ Out of Stock'}</p>
        
        <h3>Details</h3>
        <ul style="list-style: none;">
            <li>✓ High Quality Product</li>
            <li>✓ Fast Shipping Available</li>
            <li>✓ 30-Day Money Back Guarantee</li>
            <li>✓ 1-Year Warranty</li>
        </ul>
    `;
    
    document.getElementById('productDetail').innerHTML = detailsHTML;
    modal.classList.add('active');
}

function closeProductModal() {
    document.getElementById('productModal').classList.remove('active');
}

// Filter Products
function filterProducts(category) {
    currentFilter = category;
    
    // Update button states
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filter products
    if (category === 'all') {
        filteredProducts = allProducts;
    } else {
        filteredProducts = allProducts.filter(p => p.category === category);
    }
    
    renderProducts(filteredProducts);
}

// Search Products
function handleSearch(e) {
    const query = e.target.value.toLowerCase();
    
    if (query.trim() === '') {
        filteredProducts = currentFilter === 'all' ? 
            allProducts : 
            allProducts.filter(p => p.category === currentFilter);
    } else {
        const searchResults = allProducts.filter(p => 
            p.name.toLowerCase().includes(query) ||
            p.description.toLowerCase().includes(query) ||
            p.category.toLowerCase().includes(query)
        );
        
        if (currentFilter !== 'all') {
            filteredProducts = searchResults.filter(p => p.category === currentFilter);
        } else {
            filteredProducts = searchResults;
        }
    }
    
    renderProducts(filteredProducts);
}

// Add to Cart
async function addToCart(productId, productName, price) {
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${USER_ID}/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to add to cart');
        }
        
        await updateCartUI();
        showNotification(`${productName} added to cart!`, 'success');
    } catch (error) {
        console.error('Error adding to cart:', error);
        showNotification(error.message, 'error');
    }
}

// Remove from Cart
async function removeFromCart() {
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${USER_ID}/remove`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) throw new Error('Failed to remove from cart');
        
        const data = await response.json();
        showNotification(`${data.removed.name} removed from cart`, 'success');
        await updateCartUI();
    } catch (error) {
        console.error('Error removing from cart:', error);
        showNotification(error.message, 'error');
    }
}

// Clear Cart
async function clearCart() {
    if (!confirm('Are you sure you want to clear your cart?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${USER_ID}/clear`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) throw new Error('Failed to clear cart');
        
        await updateCartUI();
        showNotification('Cart cleared', 'success');
    } catch (error) {
        console.error('Error clearing cart:', error);
        showNotification(error.message, 'error');
    }
}

// Update Cart UI
async function updateCartUI() {
    try {
        const response = await fetch(`${API_BASE_URL}/cart/${USER_ID}`);
        if (!response.ok) throw new Error('Failed to fetch cart');
        
        const data = await response.json();
        const cartItems = data.items;
        const total = data.total;
        const itemCount = data.item_count;
        
        // Update cart count
        document.getElementById('cartCount').textContent = itemCount;
        
        // Update cart items display
        const cartItemsDiv = document.getElementById('cartItems');
        
        if (itemCount === 0) {
            cartItemsDiv.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
            document.getElementById('checkoutBtn').disabled = true;
        } else {
            cartItemsDiv.innerHTML = cartItems.map((item, index) => `
                <div class="cart-item">
                    <div class="cart-item-info">
                        <div class="cart-item-name">${item.name}</div>
                        <div class="cart-item-details">
                            Qty: ${item.quantity} | ${item.category}
                        </div>
                    </div>
                    <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
                    <button class="remove-btn" onclick="removeFromCart()">Remove</button>
                </div>
            `).join('');
            document.getElementById('checkoutBtn').disabled = false;
        }
        
        // Update total
        document.getElementById('cartTotal').textContent = `$${total.toFixed(2)}`;
    } catch (error) {
        console.error('Error updating cart UI:', error);
    }
}

// Checkout
async function checkout() {
    if (!confirm('Proceed to checkout?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/checkout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: USER_ID
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Checkout failed');
        }
        
        const data = await response.json();
        const order = data.order;
        
        showNotification(`✅ Order #${order.order_id} placed successfully!`, 'success');
        
        // Close cart
        toggleCart();
        
        // Update cart UI
        await updateCartUI();
        
        // Show order summary
        setTimeout(() => {
            alert(`
Order Summary:
═════════════════════════════════════
Order ID: #${order.order_id}
Total: $${order.total.toFixed(2)}
Items: ${order.items.length}
Status: ${order.status}
Time: ${new Date(order.timestamp).toLocaleString()}
═════════════════════════════════════

Thank you for your purchase! 🎉
            `);
        }, 500);
        
    } catch (error) {
        console.error('Error during checkout:', error);
        showNotification(error.message, 'error');
    }
}

// Toggle Cart
function toggleCart() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

// Show Order History
async function showOrderHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/recent-orders`);
        if (!response.ok) throw new Error('Failed to fetch orders');
        
        const orders = await response.json();
        const modal = document.getElementById('orderModal');
        const ordersList = document.getElementById('ordersList');
        
        if (orders.length === 0) {
            ordersList.innerHTML = '<p style="text-align: center; color: #7f8c8d;">No orders yet</p>';
        } else {
            ordersList.innerHTML = orders.map(order => `
                <div class="order-item">
                    <div class="order-header">
                        <span class="order-id">Order #${order.order_id}</span>
                        <span class="order-status">${order.status.toUpperCase()}</span>
                    </div>
                    <div class="order-items-list">
                        <strong>Items:</strong>
                        <ul style="margin-left: 15px;">
                            ${order.items.map(item => `
                                <li>${item.name} x${item.quantity} - $${(item.price * item.quantity).toFixed(2)}</li>
                            `).join('')}
                        </ul>
                    </div>
                    <div class="order-total">
                        Total: $${order.total.toFixed(2)}
                    </div>
                    <div style="font-size: 12px; color: #7f8c8d; margin-top: 10px;">
                        ${new Date(order.timestamp).toLocaleString()}
                    </div>
                </div>
            `).join('');
        }
        
        modal.classList.add('active');
    } catch (error) {
        console.error('Error fetching orders:', error);
        showNotification('Failed to load order history', 'error');
    }
}

function closeOrderModal() {
    document.getElementById('orderModal').classList.remove('active');
}

// Show Notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification show ${type}`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    const productModal = document.getElementById('productModal');
    const orderModal = document.getElementById('orderModal');
    
    if (e.target === productModal) {
        closeProductModal();
    }
    if (e.target === orderModal) {
        closeOrderModal();
    }
});
