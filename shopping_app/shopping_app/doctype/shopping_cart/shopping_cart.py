# Copyright (c) 2025, Princy J and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShoppingCart(Document):
    @frappe.whitelist()
    def place_order(self):
        """Create order from shopping cart"""
        
        # Step 1: Validate stock availability (Task 12)
        self.validate_stock()
        
        # Step 2: Create new Order document
        order = frappe.new_doc("Order")
        order.customer = self.customer
        order.order_status = "Pending"
        
        # Step 3: Copy cart items to order items
        for cart_item in self.cart_items:
            order.append("order_items", {
                "product": cart_item.product,
                "quantity": cart_item.quantity,
                "rate": cart_item.rate,
                "amount": cart_item.amount
            })
        
        # Step 4: Save the order (don't submit yet)
        order.insert()
        
        # Step 5: Clear the cart
        self.cart_items = []
        self.total_amount = 0
        self.save()
        
        # Step 6: Return order name for success message
        return order.name
    
    def validate_stock(self):
        """Check if sufficient stock is available"""
        
        for item in self.cart_items:
            # Get the product document
            product = frappe.get_doc("Product", item.product)
            
            # Check if enough stock
            if product.stock_qty < item.quantity:
                # Log the error before throwing
                frappe.log_error(
                    message=f"""
                    Stock Validation Failed
                    ----------------------
                    Product: {product.product_name} ({item.product})
                    Available Stock: {product.stock_qty}
                    Required Quantity: {item.quantity}
                    Shortage: {item.quantity - product.stock_qty}
                    Cart: {self.name}
                    Customer: {self.customer}
                    """,
                    title=f"Insufficient Stock - {product.product_name}"
                )
                
                # Throw error and stop the process
                frappe.throw(
                    f"Insufficient stock for {product.product_name}. "
                    f"Available: {product.stock_qty}, Required: {item.quantity}"
                )                