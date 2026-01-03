function changeMainImage(url, alt) {
    const mainImg = document.getElementById("mainProductImage");
    mainImg.src = url;
    mainImg.alt = alt;
}

function updateQuantitySelector(stock) {
    console.log('Actualizando selector con stock:', stock);
    
    const quantityContainer = document.getElementById("quantityContainer");
    
    if (!quantityContainer) {
        console.error('No se encontró quantityContainer');
        return;
    }
    
    const stockInt = parseInt(stock);
    const maxQty = Math.min(stockInt, 10);
    
    console.log('Stock procesado:', stockInt, 'Máximo:', maxQty);
    
    if (stockInt > 0) {
        let optionsHTML = '';
        for (let i = 1; i <= maxQty; i++) {
            optionsHTML += `<option value="${i}">${i}</option>`;
        }
        
        quantityContainer.innerHTML = `
            <label class="fw-bold mb-2 d-block">Cantidad:</label>
            <select id="quantitySelect" class="form-select" style="width: 150px;">
                ${optionsHTML}
            </select>
        `;
        
        console.log('Selector actualizado con', maxQty, 'opciones');
    } else {
        quantityContainer.innerHTML = '';
        console.log('Stock agotado, selector limpiado');
    }
}

function selectVariantFromData(element) {
    console.log('Variante seleccionada');
    
    const imageUrl = element.dataset.mainImage;
    const altText = element.dataset.mainAlt;
    const price = element.dataset.price;
    const discountPrice = element.dataset.discountPrice;
    const stock = element.dataset.stock;
    const images = JSON.parse(element.dataset.images);
    
    console.log('Stock de la variante:', stock);
    
    selectVariant(imageUrl, altText, price, discountPrice, stock, images);
}

function selectVariant(imageUrl, altText, price, discountPrice, stock, images) {
    console.log('=== Iniciando selectVariant ===');
    console.log('Stock recibido:', stock, 'Tipo:', typeof stock);
    
    const stockInt = parseInt(stock);
    console.log('Stock convertido:', stockInt);
    
    // Imagen principal
    changeMainImage(imageUrl, altText);

    // Miniaturas
    const thumbContainer = document.getElementById("thumbnailContainer");
    thumbContainer.innerHTML = "";

    images.forEach(img => {
        const thumb = document.createElement("img");
        thumb.src = img.url;
        thumb.alt = img.alt;
        thumb.className = "img-thumbnail product-thumb";
        thumb.style.width = "70px";
        thumb.style.height = "70px";
        thumb.style.objectFit = "cover";
        thumb.style.cursor = "pointer";
        thumb.onclick = () => changeMainImage(img.url, img.alt);
        thumbContainer.appendChild(thumb);
    });

    // Precio
    const priceContainer = document.getElementById("priceContainer");
    if (discountPrice) {
        priceContainer.innerHTML = `
            <div class="d-flex align-items-center gap-3">
                <h4 class="text-muted text-decoration-line-through" style="color:brown;">
                    $${parseFloat(price).toLocaleString('es-CO')}
                </h4>
                <h4 class="text-primary fw-bold">
                    $${parseFloat(discountPrice).toLocaleString('es-CO')}
                </h4>
            </div>
        `;
    } else {
        priceContainer.innerHTML = `
            <h4 class="text-primary fw-bold">
                $${parseFloat(price).toLocaleString('es-CO')}
            </h4>
        `;
    }

    // Stock
    const stockInfo = document.getElementById("stockInfo");
    stockInfo.innerText = "Stock disponible: " + stockInt;
    console.log('Stock actualizado en pantalla');

    // Actualizar selector de cantidad según el nuevo stock
    console.log('Llamando a updateQuantitySelector con:', stockInt);
    updateQuantitySelector(stockInt);

    // Botón de carrito
    const cartButtonContainer = document.getElementById("cartButtonContainer");
    if (stockInt > 0) {
        cartButtonContainer.innerHTML = `
            <button class="btn btn-dark w-100 mt-4 fw-bold">
                Añadir al carrito
            </button>
        `;
    } else {
        cartButtonContainer.innerHTML = `
            <button class="btn btn-danger w-100 mt-4 fw-bold" disabled>
                Producto agotado
            </button>
        `;
    }
    
    console.log('=== selectVariant completado ===');
}