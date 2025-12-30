// Copyright (c) 2025, Princy J and contributors
// For license information, please see license.txt


frappe.ui.form.on('Order', {
    refresh: function(frm) {
        // Show status badge
        if (frm.doc.order_status) {
            let color = {
                'Pending': 'orange',
                'Confirmed': 'green',
                'Packed': 'blue',
                'Shipped': 'purple',
                'Delivered': 'green',
                'Cancelled': 'red'
            };
            
            frm.dashboard.add_indicator(
                frm.doc.order_status, 
                color[frm.doc.order_status] || 'gray'
            );
        }
    },
    
    order_status: function(frm) {
        // Get old value
        let old_status = frm.doc.__onload?.old_status || 'Pending';
        let new_status = frm.doc.order_status;
        
        // If changing to Confirmed, warn about stock reduction
        if (new_status === 'Confirmed' && old_status === 'Pending') {
            frappe.msgprint({
                title: 'Stock Will Be Reduced',
                indicator: 'orange',
                message: 'Changing status to <b>Confirmed</b> will reduce stock for all items in this order.'
            });
        }
    }
});

// Logic for Order Item child table
frappe.ui.form.on('Order Item', {
    quantity: function(frm, cdt, cdn) {
        calculate_item_amount(frm, cdt, cdn);
    },
    
    rate: function(frm, cdt, cdn) {
        calculate_item_amount(frm, cdt, cdn);
    },
    
    order_items_remove: function(frm) {
        calculate_order_total(frm);
    }
});

// Helper function to calculate amount for a single item
function calculate_item_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    
    if (row.quantity && row.rate) {
        let amount = row.quantity * row.rate;
        frappe.model.set_value(cdt, cdn, 'amount', amount);
    }
    
    calculate_order_total(frm);
}

// Helper function to calculate total amount for the order
function calculate_order_total(frm) {
    let total = 0;
    
    if (frm.doc.order_items) {
        frm.doc.order_items.forEach(function(item) {
            total += item.amount || 0;
        });
    }
    
    frm.set_value('total_amount', total);
}