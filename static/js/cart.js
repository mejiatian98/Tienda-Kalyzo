// static/js/cart.js

// ================= CART UTILITIES - KALYZO SHOP =================

/**
 * Obtener token CSRF de forma robusta
 */
function getCSRFToken() {
    // 1. Intentar desde input hidden generado por {% csrf_token %}
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) {
        return csrfInput.value;
    }
    
    // 2. Intentar desde cookie
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    
    if (cookieValue) {
        return cookieValue;
    }
    
    console.error('❌ No se encontró el token CSRF');
    return null;
}

/**
 * Agregar producto al carrito desde card de producto
 */
function addToCartFromCard(event, variantId, productName) {
    event.preventDefault();
    event.stopPropagation();
    
    const button = event.currentTarget;
    const icon = button.querySelector('i');
    
    const originalIcon = icon.className;
    icon.className = 'bi bi-hourglass-split fs-4 text-primary';
    button.disabled = true;
    
    const csrfToken = getCSRFToken();
    
    if (!csrfToken) {
        showToast('Error de seguridad. Recarga la página e intenta de nuevo.', 'error');
        icon.className = originalIcon;
        button.disabled = false;
        return;
    }
    
    fetch('/orders/carrito/agregar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `variant_id=${variantId}&quantity=1`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            icon.className = 'bi bi-check-circle-fill fs-4 text-success';
            updateCartCount(data.cart_count);
            showToast(`${productName} agregado al carrito`, 'success');
            
            setTimeout(() => {
                icon.className = originalIcon;
                button.disabled = false;
            }, 1000);
        } else {
            icon.className = originalIcon;
            button.disabled = false;
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        icon.className = originalIcon;
        button.disabled = false;
        showToast('Error al agregar al carrito', 'error');
    });
}

/**
 * Actualizar cantidad de un producto en el carrito
 */
function updateCartQuantity(variantId, quantity) {
    if (quantity < 1) {
        alert('La cantidad mínima es 1');
        location.reload();
        return;
    }

    const cartItem = document.querySelector(`[data-variant-id="${variantId}"]`);
    if (cartItem) {
        cartItem.style.opacity = '0.5';
    }

    fetch('/orders/carrito/actualizar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: `variant_id=${variantId}&quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Cantidad actualizada', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast(data.message, 'error');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al actualizar el carrito', 'error');
        location.reload();
    });
}

/**
 * Eliminar producto del carrito
 */
function removeFromCart(variantId) {
    if (!confirm('¿Eliminar este producto del carrito?')) return;

    const cartItem = document.querySelector(`[data-variant-id="${variantId}"]`);
    if (cartItem) {
        cartItem.style.opacity = '0.5';
    }

    fetch('/orders/carrito/eliminar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: `variant_id=${variantId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Producto eliminado', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al eliminar del carrito', 'error');
    });
}

/**
 * Vaciar todo el carrito
 */
function clearCart() {
    if (!confirm('¿Vaciar todo el carrito?')) return;

    fetch('/orders/carrito/vaciar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Carrito vaciado', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al vaciar el carrito', 'error');
    });
}

/**
 * Actualizar contador del carrito en el header
 */
function updateCartCount(count) {
    const cartCounter = document.getElementById('cartCounter');
    if (cartCounter) {
        cartCounter.textContent = count;
        if (count > 0) {
            cartCounter.classList.remove('d-none');
        } else {
            cartCounter.classList.add('d-none');
        }
    }
}

/**
 * Mostrar notificación toast
 */
function showToast(message, type = 'info') {
    const bgColor = type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#0d6efd';
    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
    
    const toast = document.createElement('div');
    toast.className = 'position-fixed bottom-0 end-0 m-3 p-3 rounded shadow-lg text-white';
    toast.style.cssText = `
        z-index: 9999;
        background: ${bgColor};
        min-width: 250px;
        animation: slideUp 0.3s ease;
    `;
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-${icon} me-2 fs-5"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

// ================= ANIMACIONES CSS =================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from { transform: translateY(100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes slideDown {
        from { transform: translateY(0); opacity: 1; }
        to { transform: translateY(100%); opacity: 0; }
    }
    .add-to-cart-btn {
        transition: transform 0.2s ease;
    }
    .add-to-cart-btn:hover {
        transform: scale(1.1);
    }
`;
document.head.appendChild(style);

// ================= CARGAR CONTADOR DEL CARRITO AL INICIAR =================
document.addEventListener('DOMContentLoaded', function() {
    fetch('/orders/carrito/count/')
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.cart_count);
        })
        .catch(error => {
            console.error('Error al cargar contador del carrito:', error);
        });
});