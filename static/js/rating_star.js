const stars = document.querySelectorAll("#star-rating span");
const ratingInput = document.getElementById("rating-value");

stars.forEach((star, index) => {
    star.addEventListener("click", () => {
        const rating = index + 1;
        ratingInput.value = rating;

        stars.forEach((s, i) => {
            s.textContent = i < rating ? "★" : "☆";
        });
    });

    star.addEventListener("mouseover", () => {
        const hoverValue = index + 1;
        stars.forEach((s, i) => {
            s.textContent = i < hoverValue ? "★" : "☆";
        });
    });

    star.addEventListener("mouseout", () => {
        const currentRating = ratingInput.value || 0;
        stars.forEach((s, i) => {
            s.textContent = i < currentRating ? "★" : "☆";
        });
    });
});

