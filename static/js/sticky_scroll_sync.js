// static/js/sticky_scroll_sync.js

document.addEventListener('DOMContentLoaded', function() {
    const stickyElement = document.querySelector('.sidebar-sticky');
    
    if (!stickyElement) return;
    
    // Solo aplicar en desktop
    if (window.innerWidth < 992) return;
    
    let lastScrollTop = 0;
    const scrollMultiplier = 50; // El sticky scrollea 5x más rápido
    
    window.addEventListener('scroll', function() {
        // Posición actual del scroll
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
        
        // Dirección del scroll (hacia abajo o arriba)
        const scrollDirection = currentScroll > lastScrollTop ? 'down' : 'up';
        
        // Diferencia de scroll
        const scrollDelta = Math.abs(currentScroll - lastScrollTop);
        
        // Obtener el scroll actual del sticky
        const currentStickyScroll = stickyElement.scrollTop;
        const maxStickyScroll = stickyElement.scrollHeight - stickyElement.clientHeight;
        
        // Calcular nuevo scroll del sticky
        let newStickyScroll;
        
        if (scrollDirection === 'down') {
            // Scrollear hacia abajo más rápido
            newStickyScroll = currentStickyScroll + (scrollDelta * scrollMultiplier);
            // No exceder el máximo
            newStickyScroll = Math.min(newStickyScroll, maxStickyScroll);
        } else {
            // Scrollear hacia arriba más rápido
            newStickyScroll = currentStickyScroll - (scrollDelta * scrollMultiplier);
            // No ir por debajo de 0
            newStickyScroll = Math.max(newStickyScroll, 0);
        }
        
        // Aplicar el nuevo scroll al sticky
        stickyElement.scrollTop = newStickyScroll;
        
        // Guardar la posición actual
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
    }, { passive: true });
    
    // Reiniciar en resize
    window.addEventListener('resize', function() {
        if (window.innerWidth < 992) {
            stickyElement.scrollTop = 0;
        }
    });
});