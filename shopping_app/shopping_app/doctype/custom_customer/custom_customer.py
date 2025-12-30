# # Copyright (c) 2025, PrincyJ and contributors
# # For license information, please see license.txt


import frappe
from frappe.model.document import Document

class CustomCustomer(Document):
    
    def after_insert(self):
        """
        Automatically create User after Custom Customer is created
        This runs AFTER the customer is saved to database
        """
        
        # Only create user if email exists
        if self.email:
            create_user_for_customer(self)
        else:
            frappe.msgprint(
                "Customer created but User not created (no email provided)",
                indicator="orange"
            )


def create_user_for_customer(customer):
    """
    Create a User document for the customer
    """
    
    try:
        # Check if user already exists with this email
        if frappe.db.exists("User", customer.email):
            frappe.msgprint(
                f"User already exists with email: {customer.email}",
                indicator="orange"
            )
            return
        
        # Create new user
        user = frappe.new_doc("User")
        user.email = customer.email
        user.first_name = customer.customer_name
        user.username = customer.email
        
        # Set user type
        user.user_type = "Website User"  # Not a system user
        
        # Enable user
        user.enabled = 1
        
        # Send welcome email (optional - set to 0 to disable)
        user.send_welcome_email = 0
        
        # Save user
        user.insert(ignore_permissions=True)
        
        # Show success message
        frappe.msgprint(
            f"✅ User created successfully: {user.name}",
            indicator="green"
        )
    
    except Exception as e:
        # Log error but don't stop customer creation
        frappe.log_error(
            title="User Creation Failed for Customer",
            message=f"Customer: {customer.name}\nEmail: {customer.email}\n\nError: {str(e)}\n\n{frappe.get_traceback()}"
        )
        
        frappe.msgprint(
            f"⚠️ Customer created but User creation failed: {str(e)}",
            indicator="red"
        )