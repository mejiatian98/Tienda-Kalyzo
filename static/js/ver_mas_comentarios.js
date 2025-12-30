let currentIndex = 0;
const batchSize = 10;

function loadMoreComments() {
    const hiddenComments = document.getElementById('hiddenComments');
    const commentsContainer = document.getElementById('commentsContainer');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    
    if (!hiddenComments) return;
    
    const allHiddenComments = hiddenComments.querySelectorAll('.comment-item');
    const endIndex = Math.min(currentIndex + batchSize, allHiddenComments.length);
    
    // Mostrar los siguientes 10 comentarios
    for (let i = currentIndex; i < endIndex; i++) {
        const comment = allHiddenComments[i].cloneNode(true);
        comment.style.display = 'block';
        commentsContainer.insertBefore(comment, loadMoreBtn.parentElement);
    }
    
    currentIndex = endIndex;
    
    // Ocultar el botón si no hay más comentarios
    if (currentIndex >= allHiddenComments.length) {
        loadMoreBtn.parentElement.style.display = 'none';
    }
    
    // Actualizar texto del botón
    const remaining = allHiddenComments.length - currentIndex;
    if (remaining > 0) {
        loadMoreBtn.innerHTML = `Ver más comentarios (${remaining} restantes)`;
    }
}