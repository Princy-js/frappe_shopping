# Copyright (c) 2025, Princy J and contributors
# For license information, please see license.txt

import frappe


def send_order_confirmation(order_id):
    """
    Send order confirmation email (runs in background)
    This function is called by frappe.enqueue()
    """
    
    try:
        print("=" * 50)
        print("📧 SENDING ORDER CONFIRMATION EMAIL")
        print(f"Order ID: {order_id}")
        print("=" * 50)
        
        # Get order document
        order = frappe.get_doc("Order", order_id)
        
        # Get customer details
        customer = frappe.get_doc("Custom Customer", order.customer)
        
        # Get customer email
        # Check if customer has email field
        recipient_email = None
        if hasattr(customer, 'email') and customer.email:
            recipient_email = customer.email
        else:
            # If no email in customer, try to get from user
            print("⚠️ Customer has no email, trying to get from frappe.session")
            recipient_email = frappe.session.user
        
        print(f"Customer: {customer.customer_name}")
        print(f"Email: {recipient_email}")
        
        # Prepare order items list
        items_html = "<ul>"
        for item in order.order_items:
            # Get product name
            product = frappe.get_doc("Product", item.product)
            items_html += f"<li><strong>{product.product_name}</strong> - Qty: {item.quantity} - ₹{item.amount}</li>"
        items_html += "</ul>"
        
        # Prepare email message
        message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #28a745;">Order Confirmation</h2>
            
            <p>Dear <strong>{customer.customer_name}</strong>,</p>
            
            <p>Thank you for your order! Your order has been placed successfully.</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Order Details:</h3>
                <p><strong>Order Number:</strong> {order.name}</p>
                <p><strong>Order Date:</strong> {order.order_date}</p>
                <p><strong>Status:</strong> {order.order_status}</p>
            </div>
            
            <h3>Items Ordered:</h3>
            {items_html}
            
            <div style="background-color: #28a745; color: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 0; font-size: 18px;"><strong>Total Amount: ₹{order.total_amount}</strong></p>
            </div>
            
            <p>We will notify you when your order is confirmed and shipped.</p>
            
            <p>Thank you for shopping with us!</p>
            
            <hr style="margin: 30px 0;">
            
            <p style="color: #6c757d; font-size: 12px;">
                This is an automated email. Please do not reply to this email.
            </p>
        </div>
        """
        
        # Send email
        frappe.sendmail(
            recipients=[recipient_email],
            subject=f"Order Confirmation - {order.name}",
            message=message,
            delayed=False
        )
        
        print("✅ Email sent successfully!")
        print(f"Recipient: {recipient_email}")
        print("=" * 50)
        
        # Log success in Error Log (for tracking)
        frappe.log_error(
            title=f"✅ Order Email Sent - {order.name}",
            message=f"Confirmation email sent successfully to {recipient_email} for order {order_id}"
        )
    
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        print("=" * 50)
        
        # Log error
        frappe.log_error(
            title=f"❌ Order Email Failed - {order_id}",
            message=f"""
            Failed to send confirmation email for order {order_id}
            
            Error: {str(e)}
            
            Traceback:
            {frappe.get_traceback()}
            """
        )