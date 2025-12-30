// Copyright (c) 2025, Your Name and contributors
// For license information, please see license.txt

frappe.ui.form.on('Product', {
    
    // Validate when price field changes
    price: function(frm) {
        if (frm.doc.price <= 0) {
            frappe.msgprint('Price must be greater than zero', 'Invalid Price');
            frm.set_value('price', '');  // Clear the field
        }
    },
    
    // Validate before saving
    validate: function(frm) {
        if (!frm.doc.price || frm.doc.price <= 0) {
            frappe.msgprint('Please enter a valid price greater than zero');
            frappe.validated = false;  // Stop form submission
        }
    }
});