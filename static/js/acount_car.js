// Cargar el contador del carrito al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    fetch('/orders/carrito/count/')
        .then(response => response.json())
        .then(data => {
            const cartCounter = document.getElementById('cartCounter');
            if (cartCounter && data.cart_count > 0) {
                cartCounter.textContent = data.cart_count;
                cartCounter.classList.remove('d-none');
            }
        });
});