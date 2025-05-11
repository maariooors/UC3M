document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Conexión con el servidor
    
    // Para navegadores de escritorio - lo mantenemos si lo necesitas
    window.addEventListener('scroll', () => {
        if (!window.isTouching) { // Solo enviar si no es de un evento táctil
            const scrollPosition = window.scrollY;
            socket.emit('scroll', { y: scrollPosition });
        }
    });
    
    // Variables para seguimiento táctil
    let lastY = 0;
    window.isTouching = false;
    
    document.addEventListener('touchstart', (e) => {
        window.isTouching = true;
        lastY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchmove', (e) => {
        const currentTouchY = e.touches[0].clientY;
        const currentScrollY = window.scrollY;
        
        // Emitir la posición actual de scroll, no un cálculo
        socket.emit('scroll', { y: currentScrollY });
        
        // Actualizar la última posición
        lastY = currentTouchY;
    });
    
    document.addEventListener('touchend', () => {
        // Emitir posición final y marcar que el toque terminó
        const finalScrollY = window.scrollY;
        socket.emit('scroll', { y: finalScrollY });
        
        // Pequeño delay para evitar que el evento scroll normal se dispare inmediatamente
        setTimeout(() => {
            window.isTouching = false;
        }, 100);
    });
});