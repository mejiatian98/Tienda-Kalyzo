document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("featuredSlider");
    if (!slider) return;

    const items = slider.querySelectorAll(".featured-item");
    const buttons = document.querySelectorAll(".slider-btn");

    // 🔥 Si hay 3 o menos cards → ocultar botones
    if (items.length <= 3) {
        buttons.forEach(btn => btn.style.display = "none");
    }
});

function slideFeatured(direction) {
    const slider = document.getElementById("featuredSlider");
    if (!slider) return;

    const card = slider.querySelector(".featured-item");
    if (!card) return;

    const gap = 12;
    const scrollAmount = card.offsetWidth + gap;

    slider.scrollBy({
        left: direction * scrollAmount,
        behavior: "smooth"
    });
}