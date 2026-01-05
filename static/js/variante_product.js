function changeMainImage(url, alt) {
    const mainImg = document.getElementById("mainProductImage");
    mainImg.src = url;
    mainImg.alt = alt;
}

function updateQuantitySelector(stock) {
    const quantityContainer = document.getElementById("quantityContainer");
    const stockInt = parseInt(stock);
    const maxQty = Math.min(stockInt, 10);

    if (stockInt > 0) {
        let optionsHTML = "";
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
        quantityContainer.innerHTML = "";
    }
}

function selectVariantFromData(element) {
    const imageUrl = element.dataset.mainImage;
    const altText = element.dataset.mainAlt;
    const price = element.dataset.price;
    const discountPrice = element.dataset.discountPrice;
    const stock = element.dataset.stock;
    const images = JSON.parse(element.dataset.images);
    const options = JSON.parse(element.dataset.options);

    selectVariant(imageUrl, altText, price, discountPrice, stock, images, options);
}

function selectVariant(imageUrl, altText, price, discountPrice, stock, images, options) {
    const stockInt = parseInt(stock);

    // Imagen principal
    changeMainImage(imageUrl, altText);

    // Miniaturas
    const thumbContainer = document.getElementById("thumbnailContainer");
    thumbContainer.innerHTML = "";
    thumbContainer.classList.add("thumbnail-column");

    images.forEach(img => {
        const thumb = document.createElement("img");
        thumb.src = img.url;
        thumb.alt = img.alt;
        thumb.classList.add("product-thumb", "img-thumbnail");

        thumb.addEventListener("click", () => {
            document.querySelectorAll(".product-thumb").forEach(t => t.classList.remove("active"));
            thumb.classList.add("active");
            changeMainImage(img.url, img.alt);
        });

        thumbContainer.appendChild(thumb);
    });

    // Precio 
    const priceContainer = document.getElementById("priceContainer");

    if (discountPrice) {
        priceContainer.innerHTML = `
            <div class="price-line">
                <span class="price-label">Antes:</span>
                <span class="price-old">
                    $${parseFloat(price).toLocaleString('es-CO')}
                </span>
            </div>

            <div class="price-line">
                <span class="price-label">Ahora:</span>
                <span class="price-new">
                    $${parseFloat(discountPrice).toLocaleString('es-CO')}
                </span>
            </div>
        `;
    } else {
        priceContainer.innerHTML = `
            <div class="price-line">
                <span class="price-label">Precio:</span>
                <span class="price-new">
                    $${parseFloat(price).toLocaleString('es-CO')}
                </span>
            </div>
        `;
    }

    // Stock
    document.getElementById("stockInfo").innerText = "Stock disponible: " + stockInt;
    updateQuantitySelector(stockInt);

    // Botón carrito
    const cartButtonContainer = document.getElementById("cartButtonContainer");
    cartButtonContainer.innerHTML = stockInt > 0
        ? `<button class="btn btn-dark w-100 mt-4 fw-bold">Añadir al carrito</button>`
        : `<button class="btn btn-danger w-100 mt-4 fw-bold" disabled>Producto agotado</button>`;

    // ================= MEDIDAS =================
    const medidaContainer = document.getElementById("medidaContainer");
    const medidaButtons = document.getElementById("medidaButtons");

    const medidas = options.filter(o => o.option === "Medida");

    if (medidas.length > 0) {
        medidaContainer.classList.remove("d-none");
        medidaButtons.innerHTML = "";

        medidas.forEach(t => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "btn btn-outline-primary btn-sm";
            btn.innerText = t.value;

            btn.addEventListener("click", () => {
                document
                    .querySelectorAll("#medidaButtons button")
                    .forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
            });

            medidaButtons.appendChild(btn);
        });
    } else {
        medidaContainer.classList.add("d-none");
        medidaButtons.innerHTML = "";
    }
}
