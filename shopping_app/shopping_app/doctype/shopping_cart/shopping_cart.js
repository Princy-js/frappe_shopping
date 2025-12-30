// Copyright (c) 2025, PrincyJ and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shopping Cart', {
    refresh: function(frm) {
        // Add Place Order button if conditions are met
        add_place_order_button(frm);
    }
});

// Logic for Cart Item child table
frappe.ui.form.on('Cart Item', {
    // When product is selected in child table
    product: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        
        if (row.product) {
            fetch_product_details(frm, cdt, cdn, row.product);
        }
    },
    
    // When quantity changes
    quantity: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    
    // When rate changes
    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    
    // When a row is removed
    cart_items_remove: function(frm) {
        calculate_total(frm);
    }
});


// HELPER FUNCTIONS

// Add "Place Order" button to the form
function add_place_order_button(frm) {
    // Check if cart is saved and has items
    if (!frm.is_new() && frm.doc.cart_items && frm.doc.cart_items.length > 0) {
        frm.add_custom_button('Place Order', function() {
            place_order(frm);
        }).css({'background-color': '#28a745', 'color': 'white'});
    }
}

// Handle Place Order action
function place_order(frm) {
    // Show confirmation dialog
    frappe.confirm(
        'Are you sure you want to place this order?',
        function() {
            // User clicked Yes - call backend
            frappe.call({
                method: 'place_order',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint('Order ' + r.message + ' created successfully!');
                        frm.reload_doc();
                    }
                },
                error: function(r) {
                    frappe.msgprint('Error placing order. Please try again.');
                }
            });
        }
    );
}


// Fetch product details from database
function fetch_product_details(frm, cdt, cdn, product_id) {
    frappe.call({
        method: 'frappe.client.get',
        args: {
            doctype: 'Product',
            name: product_id
        },
        callback: function(r) {
            if (r.message) {
                // Set rate from product price
                frappe.model.set_value(cdt, cdn, 'rate', r.message.price);
                // Calculate amount
                calculate_amount(frm, cdt, cdn);
            }
        }
    });
}

// Calculate amount for a single cart item row
function calculate_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    
    if (row.quantity && row.rate) {
        let amount = row.quantity * row.rate;
        frappe.model.set_value(cdt, cdn, 'amount', amount);
    }
    
    // Also update the cart total
    calculate_total(frm);
}

// Calculate total amount for the entire cart
function calculate_total(frm) {
    let total = 0;
    
    // Loop through all cart items
    if (frm.doc.cart_items) {
        frm.doc.cart_items.forEach(function(item) {
            total += item.amount || 0;
        });
    }
    
    // Set the total amount in parent
    frm.set_value('total_amount', total);
}