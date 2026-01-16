// static/js/variante_product.js


// ================= VARIABLES GLOBALES =================
let currentVariantId = null;
let allVariantImages = [];

// ================= INICIALIZACIÓN =================
document.addEventListener('DOMContentLoaded', function() {
    // Guardar todas las imágenes disponibles al cargar
    const thumbs = document.querySelectorAll('.product-thumb');
    allVariantImages = Array.from(thumbs).map(thumb => ({
        url: thumb.src,
        alt: thumb.alt,
        variantId: thumb.dataset.variantId
    }));

    // Marcar la primera miniatura como activa
    if (thumbs.length > 0) {
        thumbs[0].classList.add('active');
    }

    // Obtener las opciones de la variante principal al cargar
    const mainVariantElement = document.querySelector('.variant-option.variant-selected');
    
    if (mainVariantElement) {
        const options = JSON.parse(mainVariantElement.dataset.options || '[]');
        
        // Inicializar las opciones de la variante principal
        if (typeof updateOptions === 'function') {
            updateOptions(options);
        }
    }

    // ✅ EVENT DELEGATION - Funciona con elementos dinámicos
    document.body.addEventListener('click', function(e) {
        // Si el click fue en el botón de agregar al carrito o dentro de él
        const addToCartBtn = e.target.closest('#addToCartBtn');
        if (addToCartBtn) {
            e.preventDefault();
            addToCart();
        }
    });
});

// ================= CAMBIAR IMAGEN PRINCIPAL =================
function changeMainImage(imageUrl, altText) {
    const mainImg = document.getElementById('mainProductImage');
    if (mainImg) {
        mainImg.src = imageUrl;
        mainImg.alt = altText || '';
    }

    // Actualizar miniatura activa
    document.querySelectorAll('.product-thumb').forEach(thumb => {
        thumb.classList.remove('active');
        if (thumb.src === imageUrl) {
            thumb.classList.add('active');
        }
    });
}

// ================= ACTUALIZAR PRECIO =================
function updatePrice(price, discountPrice, discountPercentage) {
    const priceContainer = document.getElementById('priceContainer');
    if (!priceContainer) return;

    const priceFloat = parseFloat(price);
    const discountFloat = discountPrice ? parseFloat(discountPrice) : null;
    const discountPercent = parseInt(discountPercentage) || 0;

    if (discountFloat && discountFloat < priceFloat) {
        priceContainer.innerHTML = `
            <div class="price-line mb-2">
                <span class="price-label me-2">Antes:</span>
                <span class="price-old">
                    $${priceFloat.toLocaleString('es-CO', {minimumFractionDigits: 0, maximumFractionDigits: 0})}
                </span>
                ${discountPercent > 0 ? `
                <span class="bg-danger text-white fw-bold px-2 py-1 rounded ms-2">
                    <small>-${discountPercent}% OFF</small>
                </span>
                ` : ''}
            </div>
            <div class="price-line">
                <span class="price-label me-2">Ahora:</span>
                <span class="price-new">
                    $${discountFloat.toLocaleString('es-CO', {minimumFractionDigits: 0, maximumFractionDigits: 0})}
                </span>
            </div>
        `;
    } else {
        priceContainer.innerHTML = `
            <div class="price-line">
                <span class="price-label me-2">Precio:</span>
                <span class="price-new">
                    $${priceFloat.toLocaleString('es-CO', {minimumFractionDigits: 0, maximumFractionDigits: 0})}
                </span>
            </div>
        `;
    }
}

// ================= ACTUALIZAR STOCK =================
function updateStock(stock) {
    const stockValue = document.getElementById('stockValue');
    if (stockValue) {
        stockValue.textContent = stock;
    }
}

// ================= ACTUALIZAR SELECTOR DE CANTIDAD =================
function updateQuantitySelector(stock) {
    const quantityContainer = document.getElementById('quantityContainer');
    if (!quantityContainer) return;

    const stockInt = parseInt(stock);

    if (stockInt > 0) {
        let optionsHTML = '';
        // ✅ GENERAR TODAS LAS OPCIONES HASTA EL STOCK DISPONIBLE
        for (let i = 1; i <= stockInt; i++) {
            optionsHTML += `<option value="${i}">${i}</option>`;
        }

        quantityContainer.innerHTML = `
            <div class="d-flex align-items-center gap-2">
                <label class="fw-bold mb-0">Cantidad:</label>
                <select id="quantitySelect" class="form-select" style="width: 150px;">
                    ${optionsHTML}
                </select>
            </div>
        `;
    } else {
        quantityContainer.innerHTML = '';
    }
}

// ================= ACTUALIZAR BOTONES =================
function updateCartButtons(stock) {
    const cartButtonContainer = document.getElementById('cartButtonContainer');
    if (!cartButtonContainer) return;

    const stockInt = parseInt(stock);

    if (stockInt > 0) {
        cartButtonContainer.innerHTML = `
            <!-- Botón secundario - Añadir al carrito -->
            <button type="button" id="addToCartBtn" class="btn bg-primary text-light w-100 fw-bold py-2 shadow-sm">
                <i class="bi bi-bag-plus fs-5 me-2"></i>
                <span class="fs-5">Añadir al carrito</span>
            </button>
            
            <!-- Botón principal - Contraentrega -->
            <button type="button" id="contraentregaBtn" class="btn bg-primary text-light w-100 fw-bold py-3 shadow-sm">
                <div class="d-flex flex-column align-items-center">
                    <div class="d-flex align-items-center mb-1">
                        <i class="bi bi-truck fs-3 me-2"></i>
                        <span class="fs-4">¡Pedir Ahora!</span>
                    </div>
                    <small class="opacity-90">Envío contraentrega gratis a todo el país</small>
                </div>
            </button>
        `;
    } else {
        cartButtonContainer.innerHTML = `
            <!-- Botón deshabilitado - Producto agotado -->
            <button class="btn btn-danger w-100 fw-bold py-3 shadow-sm" disabled>
                <i class="bi bi-x-circle fs-5 me-2"></i>
                <span class="fs-5">Producto agotado</span>
            </button>
        `;
    }
}

// ================= ACTUALIZAR OPCIONES DINÁMICAMENTE =================
function updateOptions(options) {
    // Agrupar opciones por tipo
    const optionsByType = {
        'Medida': [],
        'Peso': [],
        'Material': [],
        'Color': []
    };

    options.forEach(opt => {
        if (optionsByType[opt.option] !== undefined) {
            optionsByType[opt.option].push(opt.value);
        }
    });

    // Actualizar cada tipo de opción
    updateOptionButtons('medida', optionsByType['Medida']);
    updateOptionButtons('peso', optionsByType['Peso']);
    updateOptionButtons('material', optionsByType['Material']);
}

// ================= ACTUALIZAR BOTONES DE OPCIONES =================
function updateOptionButtons(optionType, values) {
    const container = document.getElementById(`${optionType}Container`);
    const buttonsDiv = document.getElementById(`${optionType}Buttons`);
    
    if (!container || !buttonsDiv) return;

    if (values && values.length > 0) {
        // Mostrar contenedor si tiene valores
        container.classList.remove('d-none');
        buttonsDiv.innerHTML = '';

        values.forEach(value => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-primary btn-sm';
            btn.textContent = value;

            btn.addEventListener('click', () => {
                // Remover active de todos los botones de este tipo
                document.querySelectorAll(`#${optionType}Buttons button`).forEach(b => {
                    b.classList.remove('active');
                });
                // Agregar active al botón clickeado
                btn.classList.add('active');
            });

            buttonsDiv.appendChild(btn);
        });
    } else {
        // Ocultar contenedor si no tiene valores
        container.classList.add('d-none');
        buttonsDiv.innerHTML = '';
    }
}

// ================= SELECCIONAR VARIANTE DESDE DATA =================
function selectVariantFromData(element) {
    const variantId = element.dataset.variantId;
    const imageUrl = element.dataset.mainImage;
    const altText = element.dataset.mainAlt;
    const price = element.dataset.price;
    const discountPrice = element.dataset.discountPrice;
    const discountPercentage = element.dataset.discountPercentage;
    const stock = element.dataset.stock;
    const images = JSON.parse(element.dataset.images || '[]');
    const options = JSON.parse(element.dataset.options || '[]');

    selectVariant(
        variantId,
        imageUrl,
        altText,
        price,
        discountPrice,
        discountPercentage,
        stock,
        images,
        options
    );

    // Actualizar selección visual
    document.querySelectorAll('.variant-option').forEach(opt => {
        opt.classList.remove('variant-selected');
    });
    element.classList.add('variant-selected');
}

// ================= SELECCIONAR VARIANTE PRINCIPAL =================
function selectVariant(
    variantId,
    imageUrl,
    altText,
    price,
    discountPrice,
    discountPercentage,
    stock,
    images,
    options
) {
    currentVariantId = variantId;

    // 1. Actualizar imagen principal
    changeMainImage(imageUrl, altText);

    // 2. Actualizar precio
    updatePrice(price, discountPrice, discountPercentage);

    // 3. Actualizar stock
    updateStock(stock);

    // 4. Actualizar selector de cantidad
    updateQuantitySelector(stock);

    // 5. Actualizar botones
    updateCartButtons(stock);

    // 6. Actualizar TODAS las opciones dinámicamente
    updateOptions(options);
}

// ================= FUNCIONES DEL CARRITO =================

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addToCart() {
    const variantId = currentVariantId || document.querySelector('.variant-option.variant-selected')?.dataset.variantId;
    const quantity = document.getElementById('quantitySelect')?.value || 1;
    
    if (!variantId) {
        showErrorMessage('Por favor selecciona una variante');
        return;
    }
    
    // Mostrar loading
    const btn = document.getElementById('addToCartBtn');
    if (!btn) return;
    
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Agregando...';
    btn.disabled = true;
    
    fetch('/orders/carrito/agregar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `variant_id=${variantId}&quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        btn.innerHTML = originalHTML;
        btn.disabled = false;
        
        if (data.success) {
            // Actualizar contador del carrito en el header
            updateCartCount(data.cart_count);
            
            // Mostrar mensaje de éxito
            showSuccessMessage(data.message);
            
            // Abrir el offcanvas del carrito
            setTimeout(() => {
                const carritoOffcanvas = document.getElementById('carritoOffcanvas');
                if (carritoOffcanvas) {
                    const bsOffcanvas = new bootstrap.Offcanvas(carritoOffcanvas);
                    bsOffcanvas.show();
                }
            }, 800);
        } else {
            showErrorMessage(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        btn.innerHTML = originalHTML;
        btn.disabled = false;
        showErrorMessage('Error al agregar al carrito');
    });
}

function updateCartCount(count) {
    // Actualizar el contador en el header (si existe)
    const cartCounter = document.getElementById('cartCounter');
    if (cartCounter) {
        cartCounter.textContent = count;
        if (count > 0) {
            cartCounter.classList.remove('d-none');
        }
    }
}

function showSuccessMessage(message) {
    // Crear un toast de éxito
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 start-50 translate-middle-x mt-3';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show shadow-lg" role="alert">
            <i class="bi bi-check-circle-fill me-2"></i>
            <strong>¡Éxito!</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    document.body.appendChild(toast);
    
    // Auto-remover después de 3 segundos
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function showErrorMessage(message) {
    // Crear un toast de error
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 start-50 translate-middle-x mt-3';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <div class="alert alert-danger alert-dismissible fade show shadow-lg" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Error:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    document.body.appendChild(toast);
    
    // Auto-remover después de 4 segundos
    setTimeout(() => {
        toast.remove();
    }, 4000);
}