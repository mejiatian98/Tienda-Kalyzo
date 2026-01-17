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
        // Botón de agregar al carrito
        const addToCartBtn = e.target.closest('#addToCartBtn');
        if (addToCartBtn) {
            e.preventDefault();
            addToCart();
        }
        
        // ✅ Botón de contraentrega (abre el modal)
        const contraentregaBtn = e.target.closest('#contraentregaBtn');
        if (contraentregaBtn) {
            e.preventDefault();
            handleContraentregaClick();
        }
        
        // ✅ Botón de finalizar compra
        const btnFinalizar = e.target.closest('#btnFinalizarCompra');
        if (btnFinalizar) {
            e.preventDefault();
            finalizarCompraWhatsApp();
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
                    <small class="opacity-90">Envío contraentrega y gratis a todo el país</small>
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
        container.classList.remove('d-none');
        buttonsDiv.innerHTML = '';

        values.forEach(value => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-primary btn-sm';
            btn.textContent = value;

            btn.addEventListener('click', () => {
                document.querySelectorAll(`#${optionType}Buttons button`).forEach(b => {
                    b.classList.remove('active');
                });
                btn.classList.add('active');
            });

            buttonsDiv.appendChild(btn);
        });
    } else {
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
    changeMainImage(imageUrl, altText);
    updatePrice(price, discountPrice, discountPercentage);
    updateStock(stock);
    updateQuantitySelector(stock);
    updateCartButtons(stock);
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
            updateCartCount(data.cart_count);
            showSuccessMessage(data.message);
            
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
    const cartCounter = document.getElementById('cartCounter');
    if (cartCounter) {
        cartCounter.textContent = count;
        if (count > 0) {
            cartCounter.classList.remove('d-none');
        }
    }
}

function showSuccessMessage(message) {
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
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function showErrorMessage(message) {
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
    
    setTimeout(() => {
        toast.remove();
    }, 4000);
}

// ================= CONTRAENTREGA - MODAL Y WHATSAPP =================

/**
 * Verificar si el carrito está vacío
 */
function checkCartStatus() {
    return fetch('/orders/carrito/count/')
        .then(response => response.json())
        .then(data => data.cart_count)
        .catch(error => {
            console.error('Error al verificar carrito:', error);
            return 0;
        });
}

/**
 * Manejar clic en botón de contraentrega
 * Si el carrito está vacío, primero agrega 1 producto
 */
async function handleContraentregaClick() {
    console.log('Verificando estado del carrito...');
    
    // Verificar si el carrito está vacío
    const cartCount = await checkCartStatus();
    
    if (cartCount === 0) {
        console.log('Carrito vacío, agregando producto...');
        
        // Obtener variant_id actual
        const variantId = currentVariantId || document.querySelector('.variant-option.variant-selected')?.dataset.variantId;
        
        if (!variantId) {
            showErrorMessage('Por favor selecciona una variante');
            return;
        }
        
        // Agregar producto al carrito (cantidad 1)
        try {
            const response = await fetch('/orders/carrito/agregar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `variant_id=${variantId}&quantity=1`
            });
            
            const data = await response.json();
            
            if (data.success) {
                console.log('Producto agregado exitosamente');
                updateCartCount(data.cart_count);
                showSuccessMessage('Producto agregado al carrito');
                
                // Esperar un momento y abrir el modal
                setTimeout(() => {
                    openContraentregaModal();
                }, 500);
            } else {
                showErrorMessage(data.message);
            }
        } catch (error) {
            console.error('Error al agregar producto:', error);
            showErrorMessage('Error al agregar al carrito');
        }
    } else {
        console.log('Carrito con productos, abriendo modal directamente...');
        // Si ya hay productos, abrir el modal directamente
        openContraentregaModal();
    }
}

/**
 * Abrir modal de contraentrega
 */
function openContraentregaModal() {
    console.log('Abriendo modal de contraentrega...');
    
    // Cargar resumen del pedido desde el servidor
    loadPedidoResumen();
    
    // Abrir modal
    const modalElement = document.getElementById('contraentregaModal');
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    } else {
        console.error('Modal #contraentregaModal no encontrado');
    }
}

/**
 * Cargar resumen del pedido desde el servidor
 */
function loadPedidoResumen() {
    const resumenContainer = document.getElementById('pedidoResumen');
    const totalElement = document.getElementById('totalPagar');
    
    if (!resumenContainer || !totalElement) {
        console.error('Elementos del resumen no encontrados');
        return;
    }
    
    // Mostrar loading
    resumenContainer.innerHTML = '<div class="text-center"><span class="spinner-border spinner-border-sm"></span> Cargando...</div>';
    totalElement.textContent = '$0';
    
    // Obtener datos del carrito desde el servidor
    fetch('/orders/carrito/items/')
        .then(response => response.json())
        .then(data => {
            if (!data.items || data.items.length === 0) {
                resumenContainer.innerHTML = '<p class="text-muted">No hay productos en el carrito</p>';
                totalElement.textContent = '$0';
                return;
            }
            
            let html = '<ul class="list-unstyled mb-0">';
            
            data.items.forEach(item => {
                const itemTotal = item.price * item.quantity;
                
                html += `
                    <li class="d-flex justify-content-between mb-2 pb-2 border-bottom">
                        <div>
                            <strong>${item.product_name}</strong>
                            <br>
                            <small class="text-muted">Cantidad: ${item.quantity} x $${formatNumber(item.price)}</small>
                        </div>
                        <span class="fw-bold">$${formatNumber(itemTotal)}</span>
                    </li>
                `;
            });
            
            html += '</ul>';
            resumenContainer.innerHTML = html;
            totalElement.textContent = '$' + formatNumber(data.total);
        })
        .catch(error => {
            console.error('Error al cargar pedido:', error);
            resumenContainer.innerHTML = '<p class="text-danger">Error al cargar el carrito</p>';
            totalElement.textContent = '$0';
        });
}

/**
 * Finalizar compra - Crear orden y redirigir a WhatsApp
 */
function finalizarCompraWhatsApp() {
    const form = document.getElementById('contraentregaForm');
    const btn = document.getElementById('btnFinalizarCompra');
    
    // Validar formulario
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Obtener datos del formulario
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    console.log('Datos del formulario:', data);
    
    // Mostrar loading
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Procesando...';
    btn.disabled = true;
    
    // Enviar datos al servidor para crear la orden
    fetch('/clientes/orden/crear/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(result => {
        console.log('Result:', result);
        
        if (result.success) {
            // Construir URL de WhatsApp
            const whatsappMessage = encodeURIComponent(result.data.whatsapp_message);
            const whatsappNumber = result.data.whatsapp_number;
            const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${whatsappMessage}`;
            
            console.log('WhatsApp URL:', whatsappUrl);
            
            // Abrir WhatsApp
            window.open(whatsappUrl, '_blank');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('contraentregaModal'));
            if (modal) {
                modal.hide();
            }
            
            // Mostrar mensaje de éxito
            showSuccessMessage(`¡Orden #${result.data.order_id} creada exitosamente!`);
            
            // Limpiar formulario
            form.reset();
            
            // Actualizar contador del carrito
            updateCartCount(0);
            
        } else {
            console.error('Error en result:', result.message);
            showErrorMessage(result.message || 'Error al crear la orden');
        }
        
        // Restaurar botón
        btn.innerHTML = originalHTML;
        btn.disabled = false;
    })
    .catch(error => {
        console.error('Error en fetch:', error);
        showErrorMessage('Error al procesar la compra');
        btn.innerHTML = originalHTML;
        btn.disabled = false;
    });
}

/**
 * Formatear números
 */
function formatNumber(value) {
    return Math.round(value).toLocaleString('es-CO');
}


// static/js/variante_product.js

/**
 * Finalizar compra - Crear orden y redirigir a WhatsApp
 */
function finalizarCompraWhatsApp() {
    const form = document.getElementById('contraentregaForm');
    const btn = document.getElementById('btnFinalizarCompra');
    
    // Validar formulario
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Obtener datos del formulario
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    console.log('Datos del formulario:', data);
    
    // Mostrar loading
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Procesando...';
    btn.disabled = true;
    
    // Enviar datos al servidor para crear la orden
    fetch('/clientes/orden/crear/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(result => {
        console.log('Result:', result);
        
        if (result.success) {
            // ✅ ELIMINAR COOKIE DEL CARRITO
            deleteCookie('cart');
            console.log('✅ Cookie del carrito eliminada');
            
            // Construir URL de WhatsApp
            const whatsappMessage = encodeURIComponent(result.data.whatsapp_message);
            const whatsappNumber = result.data.whatsapp_number;
            const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${whatsappMessage}`;
            
            console.log('WhatsApp URL:', whatsappUrl);
            
            // Abrir WhatsApp
            window.open(whatsappUrl, '_blank');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('contraentregaModal'));
            if (modal) {
                modal.hide();
            }
            
            // Mostrar mensaje de éxito
            showSuccessMessage(`¡Orden #${result.data.order_id} creada exitosamente!`);
            
            // Limpiar formulario
            form.reset();
            
            // Actualizar contador del carrito a 0
            updateCartCount(0);
            
            // ✅ Limpiar el contenido del offcanvas del carrito
            clearCartOffcanvas();
            
        } else {
            console.error('Error en result:', result.message);
            showErrorMessage(result.message || 'Error al crear la orden');
        }
        
        // Restaurar botón
        btn.innerHTML = originalHTML;
        btn.disabled = false;
    })
    .catch(error => {
        console.error('Error en fetch:', error);
        showErrorMessage('Error al procesar la compra');
        btn.innerHTML = originalHTML;
        btn.disabled = false;
    });
}

/**
 * ✅ Función para eliminar una cookie
 */
function deleteCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

/**
 * ✅ Limpiar el contenido del offcanvas del carrito
 */
function clearCartOffcanvas() {
    const cartItemsContainer = document.getElementById('cartItemsContainer');
    const cartTotalElement = document.getElementById('cartTotal');
    
    if (cartItemsContainer) {
        cartItemsContainer.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-cart-x fs-1 text-muted"></i>
                <p class="text-muted mt-3">Tu carrito está vacío</p>
            </div>
        `;
    }
    
    if (cartTotalElement) {
        cartTotalElement.textContent = '$0';
    }
}

/**
 * Formatear números
 */
function formatNumber(value) {
    return Math.round(value).toLocaleString('es-CO');
}