// Esperamos que el documento esté completamente cargado antes de ejecutar nuestro código
document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Conectamos al servidor vía socket
    let ultimaAlpha = null; // Último valor registrado del ángulo alpha
    const umbral = 5; // Umbral mínimo en grados para considerar que hubo un cambio de rotación significativo

    // Escuchamos los cambios de orientación del dispositivo
    window.addEventListener('deviceorientation', (event) => {
        const alpha = event.alpha; // 'alpha' es el ángulo de rotación sobre el eje Z (de 0° a 360°)

        if (alpha !== null) {
            // Si es la primera vez que recibimos un valor, solo lo guardamos
            if (ultimaAlpha === null) {
                ultimaAlpha = alpha;
                return;
            }

            // Calculamos la diferencia angular entre la orientación actual y la última
            // Esto también maneja correctamente cuando alpha cruza de 360 a 0 o viceversa
            let diff = ((alpha - ultimaAlpha + 180) % 360) - 180;

            // Si la diferencia es mayor al umbral, consideramos que hubo un movimiento relevante
            if (Math.abs(diff) > umbral) {
                const isLeft = diff > 0; // Si la diferencia es positiva, asumimos que giró a la izquierda
                
                // Enviamos al servidor la dirección del giro
                socket.emit('rotacion_movil', isLeft ? 'left' : 'right');

                // Actualizamos el último valor registrado
                ultimaAlpha = alpha;
            }
        }
    });
});
