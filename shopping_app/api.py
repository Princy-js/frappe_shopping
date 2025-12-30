# Copyright (c) 2025, Princy J and contributors
# For license information, please see license.txt
# import debugpy
# debugpy.listen(("0.0.0.0", 5678))
# print("🔴 Debugger is listening on port 5678")
# debugpy.wait_for_client()
import frappe

from shopping_app.utils.customer_utils import get_or_create_customer
from shopping_app.utils.cart_utils import (
    get_or_create_cart,
    add_product_to_cart,
    update_cart_item_quantity,
    remove_cart_item
)
from shopping_app.utils.product_utils import get_all_products
from shopping_app.utils.order_utils import (create_order_from_cart,
    cancel_order_internal)

# Get Product List API
@frappe.whitelist(allow_guest=True)
def get_products():
    
    try:
        products = get_all_products()
        
        return {
            "success": True,
            "data": products,
            "message": "Products fetched successfully"
        }
    
    except Exception as e:
        return {
            "success": False,
            "data": [],
            "message": f"Error: {str(e)}"
        }

# Add to Cart API
@frappe.whitelist()
def add_to_cart(product, quantity=1):
    # import debugpy
    # debugpy.listen(("0.0.0.0", 5678))
    # debugpy.wait_for_client()
    print("🛒 ADD TO CART FUNCTION CALLED")
    print(f"User: {frappe.session.user}")
    # breakpoint()
    try:
        # Get current user
        user = frappe.session.user

        
        if user == "Guest":
            frappe.throw("Please login to add items to cart")
        
        # Find or create customer for this user
        customer = get_or_create_customer(user)
        
        # Find or create cart for this customer
        cart = get_or_create_cart(customer)
        
        # Add product to cart
        cart = add_product_to_cart(cart, product, quantity)
        
        # Get product name for response
        product_doc = frappe.get_doc("Product", product)
        # print("🛑 BREAKPOINT: Checking product quantity")
        # breakpoint() 
        return {
            "success": True,
            "message": f"{product_doc.product_name} added to cart successfully",
            "cart_total": cart.total_amount
        }
    
    except Exception as e:
        frappe.log_error(f"Error adding to cart: {str(e)}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

# Place Order API
# @frappe.whitelist()
# def place_order(cart_name=None):
    
#     try:
#         # Get current user
#         user = frappe.session.user
        
#         if user == "Guest":
#             frappe.throw("Please login to place order")
        
#         # Get cart
#         if cart_name:
#             cart = frappe.get_doc("Shopping Cart", cart_name)
#         else:
#             # Find customer and cart for current user
#             customer = get_or_create_customer(user)
#             cart = get_or_create_cart(customer)
        
#         # Create order from cart
#         order = create_order_from_cart(cart)
        
#         return {
#             "success": True,
#             "message": f"Order {order.name} placed successfully",
#             "order_name": order.name,
#             "order_status": order.order_status,
#             "total_amount": order.total_amount
#         }
    
#     except Exception as e:
#         frappe.log_error(f"Error placing order: {str(e)}")
#         return {
#             "success": False,
#             "message": f"Error: {str(e)}"
#         }

# Place Order API
@frappe.whitelist()
def place_order(cart_name=None):
    """Place order and send confirmation email in background"""
    
    try:
        # Get current user
        user = frappe.session.user
        
        if user == "Guest":
            frappe.throw("Please login to place order")
        
        # Get cart
        if cart_name:
            cart = frappe.get_doc("Shopping Cart", cart_name)
        else:
            # Find customer and cart for current user
            customer = get_or_create_customer(user)
            cart = get_or_create_cart(customer)
        
        # Check if cart has items
        if not cart.cart_items or len(cart.cart_items) == 0:
            return {
                "success": False,
                "message": "Cart is empty"
            }
        
        # Create order from cart
        order = create_order_from_cart(cart)
        
        # ✅ Send confirmation email in background (NEW!)
        frappe.enqueue(
            method='shopping_app.utils.email_utils.send_order_confirmation',
            queue='short',
            timeout=300,
            order_id=order.name
        )
        
        return {
            "success": True,
            "message": f"Order {order.name} placed successfully! Confirmation email will arrive shortly.",
            "order_name": order.name,
            "order_status": order.order_status,
            "total_amount": order.total_amount
        }
    
    except Exception as e:
        frappe.log_error(
            title="Place Order Failed",
            message=frappe.get_traceback()
        )
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

# Update Cart Item Quantity API
@frappe.whitelist()
def update_cart_quantity(product, quantity):
    
    try:
        user = frappe.session.user
        
        if user == "Guest":
            frappe.throw("Please login")
        
        # Get customer and cart
        customer = get_or_create_customer(user)
        cart = get_or_create_cart(customer)
        
        # Update item quantity
        cart = update_cart_item_quantity(cart, product, quantity)
        
        return {
            "success": True,
            "message": "Cart updated successfully",
            "cart_total": cart.total_amount
        }
    
    except Exception as e:
        frappe.log_error(f"Error updating cart: {str(e)}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

# Remove Item from Cart API
@frappe.whitelist()
def remove_from_cart(product):
    
    try:
        user = frappe.session.user
        
        if user == "Guest":
            frappe.throw("Please login")
        
        # Get customer and cart
        customer = get_or_create_customer(user)
        cart = get_or_create_cart(customer)
        
        # Remove item from cart
        cart = remove_cart_item(cart, product)
        
        return {
            "success": True,
            "message": "Item removed from cart",
            "cart_total": cart.total_amount
        }
    
    except Exception as e:
        frappe.log_error(f"Error removing from cart: {str(e)}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

#cancel order
@frappe.whitelist()
def cancel_order(order_name):

    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw("Please login")
        
        customer = get_or_create_customer(user)
        result = cancel_order_internal(order_name, customer)
        
        return {
            "success": True,
            "message": result
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


