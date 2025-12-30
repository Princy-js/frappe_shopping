import frappe

def get_context(context):
    # Fetch all products and pass to template
    
    # Fetch all products from database (including out of stock)
    context.products = frappe.get_all(
        "Product",
        fields=["name", "product_name", "price", "product_image", "stock_qty"],
        order_by="product_name"
    )
    
    # Set page title
    context.title = "Shop"
    
    return context