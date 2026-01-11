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
            <div class="price-line">
                <span class="price-label">Antes:</span>
                <span class="price-old">
                    $${priceFloat.toLocaleString('es-CO', {minimumFractionDigits: 0, maximumFractionDigits: 0})}
                </span>
                ${discountPercent > 0 ? `
                <span class="bg-danger text-white fw-bold p-1 rounded d-inline-block small">
                    <small>-${discountPercent}% Descuento</small>
                </span>
                ` : ''}
            </div>
            <div class="price-line">
                <span class="price-label">Ahora:</span>
                <span class="price-new">
                    $${discountFloat.toLocaleString('es-CO', {minimumFractionDigits: 0, maximumFractionDigits: 0})}
                </span>
            </div>
        `;
    } else {
        priceContainer.innerHTML = `
            <div class="price-line">
                <span class="price-label">Precio:</span>
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
    const maxQty = Math.min(stockInt, 10);

    if (stockInt > 0) {
        let optionsHTML = '';
        for (let i = 1; i <= maxQty; i++) {
            optionsHTML += `<option value="${i}">${i}</option>`;
        }

        quantityContainer.innerHTML = `
            <label class="fw-bold mb-2 d-block">Cantidad:</label>
            <select id="quantitySelect" class="form-select" style="width:150px;">
                ${optionsHTML}
            </select>
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
            <a href="#" id="contraentregaBtn">
                <button class="btn btn-primary w-100 fw-bold mt-2 fs-2">
                    ¡Pedir Contraentrega!
                    <p><small>Envío gratis!</small></p>
                </button>
            </a>
            <a href="#" id="addToCartBtn">
                <button class="btn btn-primary w-100 fw-bold mt-2 fs-4">
                    <i class="bi bi-bag-plus"></i>
                    Añadir al carrito
                </button>
            </a>
        `;
    } else {
        cartButtonContainer.innerHTML = `
            <button class="btn btn-danger w-100 fw-bold" disabled>
                Producto agotado 
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

    // 2. ✅ YA NO ACTUALIZAMOS LAS MINIATURAS - Se mantienen todas las imágenes
    // updateThumbnails(images); // ← LÍNEA ELIMINADA

    // 3. Actualizar precio
    updatePrice(price, discountPrice, discountPercentage);

    // 4. Actualizar stock
    updateStock(stock);

    // 5. Actualizar selector de cantidad
    updateQuantitySelector(stock);

    // 6. Actualizar botones
    updateCartButtons(stock);

    // 7. Actualizar TODAS las opciones dinámicamente
    updateOptions(options);
}

// ================= INICIALIZAR OPCIONES DE LA VARIANTE PRINCIPAL AL CARGAR =================
document.addEventListener('DOMContentLoaded', function() {
    // Obtener las opciones de la variante principal al cargar
    const mainVariantElement = document.querySelector('.variant-option.variant-selected');
    
    if (mainVariantElement) {
        const options = JSON.parse(mainVariantElement.dataset.options || '[]');
        
        // Inicializar las opciones de la variante principal
        if (typeof updateOptions === 'function') {
            updateOptions(options);
        }
    }
});