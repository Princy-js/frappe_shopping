# Copyright (c) 2025, Princy J and contributors
# For license information, please see license.txt

import frappe


def validate_stock_availability(cart_items):

    for item in cart_items:
        product = frappe.get_doc("Product", item.product)
        
        if product.stock_qty < item.quantity:
            frappe.throw(
                f"Insufficient stock for {product.product_name}. "
                f"Available: {product.stock_qty}, Required: {item.quantity}"
            )


def reduce_product_stock(product_name, quantity):
    
    product = frappe.get_doc("Product", product_name)
    
    if product.stock_qty < quantity:
        frappe.throw(
            f"Insufficient stock for {product.product_name}. "
            f"Available: {product.stock_qty}, Required: {quantity}"
        )
    
    product.stock_qty -= quantity
    product.save()
