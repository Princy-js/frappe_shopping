
# Copyright (c) 2025, Princy J and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Order(Document):
    def before_save(self):
        """Calculate total before saving"""
        try:
            # DEBUGGING
            print("=" * 50)
            print("📝 Order.before_save() called")
            print(f"Order: {self.name}")
            print(f"Customer: {self.customer}")
            print(f"Status: {self.order_status}")
            print(f"Items count: {len(self.order_items)}")
            print("=" * 50)
            
            self.calculate_total()
            
        except Exception as e:
            frappe.log_error(
                title="Order before_save Error",
                message=frappe.get_traceback()
            )
            frappe.throw(f"Error calculating order total: {str(e)}")
    
    def validate(self):
        """Check if status changed and handle stock"""
        # Check if this is an update (not new document)
        if not self.is_new():
            # Get old status from database
            old_doc = self.get_doc_before_save()
            
            if old_doc:
                old_status = old_doc.order_status
                new_status = self.order_status
                
                print(f"Status change: {old_status} → {new_status}")
                
                # If status changed from Pending to Confirmed
                if old_status == "Pending" and new_status == "Confirmed":
                    print("⚡ Status changed to Confirmed - Reducing stock!")
                    self.reduce_stock()
                
                # If status changed from Confirmed back to Pending
                elif old_status == "Confirmed" and new_status == "Pending":
                    frappe.msgprint(
                        "Warning: Changing from Confirmed to Pending. Stock was already reduced!",
                        indicator="orange"
                    )
    
    def calculate_total(self):
        """Calculate total amount from order items"""
        total = 0
        for item in self.order_items:
            if item.amount:
                total += item.amount
        
        self.total_amount = total
    
    def reduce_stock(self):
        """Reduce product stock quantities"""
        for item in self.order_items:
            # Get the product
            product = frappe.get_doc("Product", item.product)
            
            # Check if sufficient stock
            if product.stock_qty < item.quantity:
                frappe.throw(
                    f"Insufficient stock for {product.product_name}. "
                    f"Available: {product.stock_qty}, Required: {item.quantity}"
                )
            
            # Reduce the stock
            product.stock_qty -= item.quantity
            product.save()
            
            frappe.msgprint(f"Stock reduced for {product.product_name}: {item.quantity} units")
            print(f"✅ Stock reduced for {product.product_name}: {item.quantity} units")
            
            # Log stock reduction
            frappe.log_error(
                message=f"Stock reduced: {product.product_name} - Qty: {item.quantity}, New Stock: {product.stock_qty}",
                title=f"Stock Reduced - {self.name}"
            )