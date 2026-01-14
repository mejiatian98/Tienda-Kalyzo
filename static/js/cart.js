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
            
            // Abrir el offcanvas del carrito después de mostrar el mensaje
            setTimeout(() => {
                icon.className = originalIcon;
                button.disabled = false;
                
                const carritoOffcanvas = document.getElementById('carritoOffcanvas');
                if (carritoOffcanvas) {
                    const bsOffcanvas = new bootstrap.Offcanvas(carritoOffcanvas);
                    bsOffcanvas.show();
                }
            }, 800);
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
        showToast('La cantidad mínima es 1', 'error');
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
            
            // Verificar si estamos en el offcanvas
            const offcanvasElement = document.getElementById('carritoOffcanvas');
            const isOffcanvasOpen = offcanvasElement && offcanvasElement.classList.contains('show');
            
            if (isOffcanvasOpen) {
                // Si está en el offcanvas, recargar y mantenerlo abierto
                setTimeout(() => {
                    location.href = location.href + '?offcanvas=open';
                }, 500);
            } else {
                // Si está en la página del carrito, solo recargar
                setTimeout(() => location.reload(), 500);
            }
        } else {
            showToast(data.message, 'error');
            if (cartItem) {
                cartItem.style.opacity = '1';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al actualizar el carrito', 'error');
        if (cartItem) {
            cartItem.style.opacity = '1';
        }
    });
}

/**
 * Eliminar producto del carrito
 */
function removeFromCart(variantId) {
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
            showToast('Producto eliminado del carrito', 'success');
            
            // Verificar si estamos en el offcanvas
            const offcanvasElement = document.getElementById('carritoOffcanvas');
            const isOffcanvasOpen = offcanvasElement && offcanvasElement.classList.contains('show');
            
            if (isOffcanvasOpen) {
                // Si está en el offcanvas, recargar y mantenerlo abierto
                setTimeout(() => {
                    location.href = location.href + '?offcanvas=open';
                }, 500);
            } else {
                // Si está en la página del carrito, solo recargar
                setTimeout(() => location.reload(), 500);
            }
        } else {
            showToast(data.message, 'error');
            if (cartItem) {
                cartItem.style.opacity = '1';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al eliminar del carrito', 'error');
        if (cartItem) {
            cartItem.style.opacity = '1';
        }
    });
}

/**
 * Vaciar todo el carrito
 */
function clearCart() {
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
            showToast('Carrito vaciado correctamente', 'success');
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
    const config = {
        success: {
            bg: '#28a745',
            icon: 'check-circle-fill'
        },
        error: {
            bg: '#dc3545',
            icon: 'exclamation-triangle-fill'
        },
        info: {
            bg: '#0d6efd',
            icon: 'info-circle-fill'
        }
    };
    
    const { bg, icon } = config[type] || config.info;
    
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 start-50 translate-middle-x mt-3';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show shadow-lg" role="alert" style="min-width: 300px;">
            <i class="bi bi-${icon} me-2"></i>
            <strong>${type === 'success' ? '¡Éxito!' : type === 'error' ? 'Error:' : 'Info:'}</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remover después de 3 segundos
    setTimeout(() => {
        toast.remove();
    }, 3000);
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
    // Cargar contador
    fetch('/orders/carrito/count/')
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.cart_count);
        })
        .catch(error => {
            console.error('Error al cargar contador del carrito:', error);
        });
    
    // Verificar si debe abrir el offcanvas (después de actualizar cantidad)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('offcanvas') === 'open') {
        const carritoOffcanvas = document.getElementById('carritoOffcanvas');
        if (carritoOffcanvas) {
            const bsOffcanvas = new bootstrap.Offcanvas(carritoOffcanvas);
            bsOffcanvas.show();
        }
        
        // Limpiar la URL sin recargar
        const cleanUrl = window.location.pathname + window.location.hash;
        window.history.replaceState({}, document.title, cleanUrl);
    }
});