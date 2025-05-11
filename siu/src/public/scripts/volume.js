// Esperamos a que el contenido del DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
    // Nos conectamos al servidor usando socket.io
    const socket = io();

    // Variables para manejar el estado del toque y la orientación inicial del dispositivo
    let tocando = false, initialBeta = null;

    // Sensibilidad para detectar un cambio en la inclinación (cuanto más bajo, más sensible)
    const SENSIBILIDAD = 10;

    // Evento que se dispara cuando tocamos la pantalla
    document.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Prevenimos el comportamiento por defecto (como scroll)
        tocando = true;  // Marcamos que se está tocando la pantalla
        initialBeta = null; // Reiniciamos la orientación inicial
    }, { passive: false }); // Necesitamos `passive: false` para que `preventDefault()` funcione

    // Evento que se dispara cuando dejamos de tocar la pantalla
    document.addEventListener('touchend', () => { 
        tocando = false; // Ya no se está tocando la pantalla
    }, { passive: true });

    // Si el navegador soporta eventos de orientación del dispositivo...
    window.DeviceOrientationEvent && window.addEventListener('deviceorientation', (e) => {
        // Solo procesamos si se está tocando la pantalla y hay un valor válido de orientación en el eje beta (inclinación adelante/atrás)
        if (tocando && e.beta !== null) {
            // Si es la primera vez que capturamos beta, la guardamos como referencia
            if (initialBeta === null) {
                initialBeta = e.beta;
                return;
            }
            
            // Calculamos la diferencia entre la orientación actual y la inicial
            const diferencia = e.beta - initialBeta;
            
            // Si esa diferencia supera la sensibilidad definida, enviamos una señal al servidor
            if (Math.abs(diferencia) > SENSIBILIDAD) {
                // Enviamos al servidor si el movimiento fue hacia adelante (positivo) o hacia atrás (negativo)
                socket.emit("volumen", diferencia > 0);

                // Actualizamos la referencia para que no dispare continuamente por un solo movimiento largo
                initialBeta = e.beta;
            }
        }
    }, { passive: true }); // Usamos passive aquí para mejorar el rendimiento del scroll en móviles
});
