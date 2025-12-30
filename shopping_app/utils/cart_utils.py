# Copyright (c) 2025, Princy J and contributors
# For license information, please see license.txt

import frappe

# Get logger
# logger = frappe.logger("shopping_app.cart")
logger = frappe.logger(
    "shopping_app.cart",
    allow_site=True
)

def get_or_create_cart(customer):
    
    # Check if cart exists
    cart_name = frappe.db.get_value("Shopping Cart", {"customer": customer}, "name")
    
    if cart_name:
        return frappe.get_doc("Shopping Cart", cart_name)
    
    # Create new cart
    cart = frappe.new_doc("Shopping Cart")
    cart.customer = customer
    cart.total_amount = 0
    cart.insert(ignore_permissions=True)
    
    return cart


def add_product_to_cart(cart, product, quantity):
    # Get product details
    product_doc = frappe.get_doc("Product", product)
    #
    logger.warning(f"Product details: {product_doc.product_name}, Price: {product_doc.price}, Stock: {product_doc.stock_qty}")
        
    # Check if product already exists in cart
    existing_item = find_cart_item(cart, product)
    
    if existing_item:
        # Update quantity
        existing_item.quantity += int(quantity)
        existing_item.amount = existing_item.quantity * existing_item.rate
    else:
        # Add new item to cart
        cart.append("cart_items", {
            "product": product,
            "quantity": int(quantity),
            "rate": product_doc.price,
            "amount": product_doc.price * int(quantity)
        })
    
    # Recalculate total
    recalculate_cart_total(cart)
    cart.save()
    
    return cart


def find_cart_item(cart, product):
   
    for item in cart.cart_items:
        if item.product == product:
            return item
    return None


def update_cart_item_quantity(cart, product, quantity):
   
    item_found = False
    item_to_remove = None
    
    for item in cart.cart_items:
        if item.product == product:
            item_found = True
            new_qty = int(quantity)
            
            if new_qty <= 0:
                # Mark for removal
                item_to_remove = item
            else:
                item.quantity = new_qty
                item.amount = item.quantity * item.rate
            
            break
    
    # Remove item if needed
    if item_to_remove:
        cart.cart_items.remove(item_to_remove)
    
    if not item_found:
        frappe.throw("Product not found in cart")
    
    # Recalculate total
    recalculate_cart_total(cart)
    cart.save()
    
    return cart


def remove_cart_item(cart, product):

    item_to_remove = None
    
    for item in cart.cart_items:
        if item.product == product:
            item_to_remove = item
            break
    
    if item_to_remove:
        cart.cart_items.remove(item_to_remove)
    
    # Recalculate total
    recalculate_cart_total(cart)
    cart.save()
    
    return cart


def recalculate_cart_total(cart):
    
    total = sum(item.amount for item in cart.cart_items)
    cart.total_amount = total


def clear_cart(cart):
    
    cart.cart_items = []
    cart.total_amount = 0
    cart.save()
    return cart
