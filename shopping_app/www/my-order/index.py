import frappe
from frappe import _

def get_context(context):
    """Display user's orders"""
    
    # Check if user is logged in
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to view your orders"), frappe.PermissionError)
    
    # Get current user
    user = frappe.session.user
    
    # Get real orders
    orders = get_user_orders(user)
    
    context.orders = orders
    context.title = "My Orders"
    
    return context


def get_user_orders(user):
    """Get all orders for logged in user"""
    
    # Find customer linked to this user
    customer = None
    
    # Try to find by checking if Custom Customer has email field
    if frappe.db.has_column("Custom Customer", "email"):
        customer = frappe.db.get_value("Custom Customer", {"email": user}, "name")
    
    # If not found, try matching with customer_name
    if not customer:
        customer = frappe.db.get_value("Custom Customer", {"customer_name": user}, "name")
    
    if not customer:
        return []
    
    # Get all orders for this customer
    orders = frappe.get_all(
        "Order",
        filters={"customer": customer},
        fields=["name", "order_date", "total_amount", "order_status"],
        order_by="creation desc"  # Latest orders first
    )
    
    # Get order items for each order
    orders_with_items = []
    for order in orders:
        # Get full order document
        order_doc = frappe.get_doc("Order", order.name)
        
        # Prepare order items
        order_items = []
        for item in order_doc.order_items:
            # Get product details
            product = frappe.get_doc("Product", item.product)
            
            order_items.append({
                "product_name": product.product_name,
                "quantity": item.quantity,
                "rate": item.rate,
                "amount": item.amount
            })
        
        # Add to orders list
        orders_with_items.append({
            "name": order.name,
            "order_date": order.order_date,
            "total_amount": order.total_amount,
            "order_status": order.order_status,
            "order_items": order_items
        })
    
    return orders_with_items