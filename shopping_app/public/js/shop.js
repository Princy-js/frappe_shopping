// Shop Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Add click event to all "Add to Cart" buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            addToCart(this);
        });
    });
});

function addToCart(button) {
    let productId = button.getAttribute('data-product');
    let productName = button.getAttribute('data-product-name');
    let price = button.getAttribute('data-price');
    
    // Show loading state
    button.disabled = true;
    button.textContent = 'Adding...';
    
    // Call backend to add to cart
    frappe.call({
        method: 'shopping_app.api.add_to_cart',
        args: {
            product: productId,
            quantity: 1
        },
        callback: function(response) {
            if (response.message) {
                frappe.show_alert({
                    message: productName + ' added to cart!',
                    indicator: 'green'
                });
                resetButton(button);
            }
        },
        error: function(error) {
            frappe.show_alert({
                message: 'Please login to add items to cart',
                indicator: 'red'
            });
            resetButton(button);
        }
    });
}

function resetButton(button) {
    button.disabled = false;
    button.textContent = 'Add to Cart';
}