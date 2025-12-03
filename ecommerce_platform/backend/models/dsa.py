# Data Structures for E-commerce Platform

class Node:
    """Node for Linked List"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Linked List implementation for storing orders"""
    def __init__(self):
        self.head = None
    
    def append(self, data):
        """Add item to end of list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def to_list(self):
        """Convert linked list to Python list"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def remove(self, data):
        """Remove item from list"""
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

class Queue:
    """Queue implementation for shopping cart (FIFO)"""
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Add item to queue"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return item from queue"""
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Get queue size"""
        return len(self.items)
    
    def get_items(self):
        """Get all items"""
        return self.items
    
    def clear(self):
        """Clear all items"""
        self.items = []

class BinarySearchTree:
    """BST for efficient product lookup by ID"""
    class TreeNode:
        def __init__(self, product_id, product):
            self.product_id = product_id
            self.product = product
            self.left = None
            self.right = None
    
    def __init__(self):
        self.root = None
    
    def insert(self, product_id, product):
        """Insert product into BST"""
        if self.root is None:
            self.root = self.TreeNode(product_id, product)
        else:
            self._insert_recursive(self.root, product_id, product)
    
    def _insert_recursive(self, node, product_id, product):
        if product_id < node.product_id:
            if node.left is None:
                node.left = self.TreeNode(product_id, product)
            else:
                self._insert_recursive(node.left, product_id, product)
        elif product_id > node.product_id:
            if node.right is None:
                node.right = self.TreeNode(product_id, product)
            else:
                self._insert_recursive(node.right, product_id, product)
    
    def search(self, product_id):
        """Search for product by ID"""
        return self._search_recursive(self.root, product_id)
    
    def _search_recursive(self, node, product_id):
        if node is None:
            return None
        if product_id == node.product_id:
            return node.product
        elif product_id < node.product_id:
            return self._search_recursive(node.left, product_id)
        else:
            return self._search_recursive(node.right, product_id)
    
    def inorder_traversal(self):
        """Get all products in sorted order by ID"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.product)
            self._inorder_recursive(node.right, result)

class InventoryArray:
    """Array-based inventory management (product_id -> stock)"""
    def __init__(self):
        self.inventory = []  # List of [product_id, stock] pairs
    
    def insert(self, product_id, stock):
        """Insert or update inventory"""
        for i, (pid, _) in enumerate(self.inventory):
            if pid == product_id:
                self.inventory[i] = [product_id, stock]
                return
        self.inventory.append([product_id, stock])
    
    def search(self, product_id):
        """Get stock for product"""
        for pid, stock in self.inventory:
            if pid == product_id:
                return stock
        return None
    
    def delete(self, product_id):
        """Remove product from inventory"""
        self.inventory = [[pid, stock] for pid, stock in self.inventory if pid != product_id]
    
    def get_all(self):
        """Get all inventory items as dictionary"""
        result = {}
        for pid, stock in self.inventory:
            result[pid] = stock
        return result

class Stack:
    """Stack for order history (LIFO)"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to stack"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """View top item without removing"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self.items) == 0
    
    def size(self):
        """Get stack size"""
        return len(self.items)
    
    def get_items(self):
        """Get all items"""
        return self.items[::-1]  # Return in order from most recent
