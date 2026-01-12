// ================= SISTEMA DE ESTRELLAS =================
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('#star-rating span');
    const ratingInput = document.getElementById('rating-value');
    
    stars.forEach(star => {
        // Click para seleccionar
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            ratingInput.value = value;
            
            // Actualizar todas las estrellas
            stars.forEach(s => {
                s.textContent = '☆';
                s.classList.remove('filled');
            });
            
            // Llenar hasta la seleccionada
            for (let i = 0; i < value; i++) {
                stars[i].textContent = '★';
                stars[i].classList.add('filled');
            }
        });

        // Hover preview
        star.addEventListener('mouseenter', function() {
            const value = this.getAttribute('data-value');
            stars.forEach((s, index) => {
                if (index < value) {
                    s.textContent = '★';
                } else {
                    s.textContent = '☆';
                }
            });
        });
    });

    // Restaurar al salir del hover
    const starRating = document.getElementById('star-rating');
    starRating.addEventListener('mouseleave', function() {
        const currentValue = ratingInput.value;
        stars.forEach((s, index) => {
            if (currentValue && index < currentValue) {
                s.textContent = '★';
            } else {
                s.textContent = '☆';
            }
        });
    });
});

// ================= CARGAR MÁS COMENTARIOS =================
function loadMoreComments() {
    const hiddenComments = document.getElementById('hiddenComments');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const commentsContainer = document.getElementById('commentsContainer');
    
    if (hiddenComments) {
        const comments = hiddenComments.querySelectorAll('.comment-item');
        comments.forEach(comment => {
            commentsContainer.appendChild(comment.cloneNode(true));
        });
        hiddenComments.style.display = 'none';
        loadMoreBtn.style.display = 'none';
    }
}