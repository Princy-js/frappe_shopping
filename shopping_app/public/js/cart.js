// document.addEventListener('DOMContentLoaded', function() {
    
//     // Increase Quantity Buttons
//     document.querySelectorAll('.increase-qty-btn').forEach(function(button) {
//         button.addEventListener('click', function() {
//             let productId = this.getAttribute('data-product');
//             let currentQty = parseInt(this.parentElement.querySelector('span strong').textContent);
//             updateQuantity(productId, currentQty + 1);
//         });
//     });
    
//     // Decrease Quantity Buttons
//     document.querySelectorAll('.decrease-qty-btn').forEach(function(button) {
//         button.addEventListener('click', function() {
//             let productId = this.getAttribute('data-product');
//             let currentQty = parseInt(this.parentElement.querySelector('span strong').textContent);
            
//             if (currentQty <= 1) {
//                 removeFromCart(productId);
//             } else {
//                 updateQuantity(productId, currentQty - 1);
//             }
//         });
//     });
    
//     // Remove Item Buttons
//     document.querySelectorAll('.remove-item-btn').forEach(function(button) {
//         button.addEventListener('click', function() {
//             let productId = this.getAttribute('data-product');
//             removeFromCart(productId);
//         });
//     });
    
//     // Place Order Button
//     const placeOrderBtn = document.getElementById('place-order-btn');
//     if (placeOrderBtn) {
//         placeOrderBtn.addEventListener('click', function() {
//             placeOrder();
//         });
//     }
// });

// function updateQuantity(productId, newQty) {
//     frappe.call({
//         method: 'shopping_app.api.update_cart_quantity',
//         args: {
//             product: productId,
//             quantity: newQty
//         },
//         callback: function(r) {
//             if (r.message && r.message.success) {
//                 frappe.show_alert({
//                     message: 'Quantity updated',
//                     indicator: 'green'
//                 });
//                 setTimeout(function() {
//                     window.location.reload();
//                 }, 500);
//             } else {
//                 frappe.show_alert({
//                     message: r.message.message || 'Error updating cart',
//                     indicator: 'red'
//                 });
//             }
//         }
//     });
// }

// function removeFromCart(productId) {
//     frappe.confirm(
//         'Remove this item from cart?',
//         function() {
//             frappe.call({
//                 method: 'shopping_app.api.remove_from_cart',
//                 args: {
//                     product: productId
//                 },
//                 callback: function(r) {
//                     if (r.message && r.message.success) {
//                         frappe.show_alert({
//                             message: 'Item removed from cart',
//                             indicator: 'orange'
//                         });
//                         setTimeout(function() {
//                             window.location.reload();
//                         }, 1000);
//                     }
//                 }
//             });
//         }
//     );
// }

// function placeOrder() {
//     frappe.confirm(
//         'Are you sure you want to place this order?',
//         function() {
//             frappe.show_alert({
//                 message: 'Placing order...',
//                 indicator: 'blue'
//             });
            
//             frappe.call({
//                 method: 'shopping_app.api.place_order',
//                 callback: function(r) {
//                     if (r.message && r.message.success) {
//                         frappe.show_alert({
//                             message: r.message.message,
//                             indicator: 'green'
//                         });
//                         setTimeout(function() {
//                             window.location.href = '/my-order';
//                         }, 2000);
//                     }
//                 }
//             });
//         }
//     );
// }