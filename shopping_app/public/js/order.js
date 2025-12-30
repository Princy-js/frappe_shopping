// My Orders Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // View Order Details Buttons
    document.querySelectorAll('.view-order-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            let orderId = this.getAttribute('data-order');
            viewOrderDetails(orderId);
        });
    });
    
    // Cancel Order Buttons
    document.querySelectorAll('.cancel-order-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            let orderId = this.getAttribute('data-order');
            cancelOrder(orderId);
        });
    });
});

/**
 * View order details (placeholder for future enhancement)
 */
function viewOrderDetails(orderId) {
    frappe.msgprint({
        title: 'Order Details',
        message: 'Viewing details for order: ' + orderId,
        indicator: 'blue'
    });
}

/**
 * Cancel an order
 */
function cancelOrder(orderId) {
    frappe.confirm(
        'Are you sure you want to cancel order ' + orderId + '?',
        function() {
            // User confirmed - call API
            frappe.call({
                method: 'shopping_app.api.cancel_order',
                args: {
                    order_name: orderId
                },
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.show_alert({
                            message: r.message.message,
                            indicator: 'orange'
                        });
                        
                        // Reload page after 1.5 seconds to show updated status
                        setTimeout(function() {
                            window.location.reload();
                        }, 1500);
                    } else {
                        frappe.show_alert({
                            message: r.message.message || 'Error cancelling order',
                            indicator: 'red'
                        });
                    }
                },
                error: function(err) {
                    console.error('Cancel order error:', err);
                    frappe.show_alert({
                        message: 'Error cancelling order. Please try again.',
                        indicator: 'red'
                    });
                }
            });
        }
    );
}