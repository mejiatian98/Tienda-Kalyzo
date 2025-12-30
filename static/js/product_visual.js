function changeMainImage(imageUrl, altText) {
    const mainImage = document.getElementById("mainProductImage");
    mainImage.src = imageUrl;
    mainImage.alt = altText;
}