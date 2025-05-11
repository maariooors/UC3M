// Esperamos a que todo el contenido del DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Iniciamos conexión con el servidor
    let ultimoEstado = null; // Para guardar el último estado enviado (evitar repeticiones innecesarias)

    // Verificamos si el navegador soporta eventos de orientación del dispositivo
    if (window.DeviceOrientationEvent) {
        window.addEventListener("deviceorientation", (event) => {
            const beta = event.beta; // beta es el ángulo de inclinación frontal-trasera

            // Determinamos si el teléfono está con la pantalla hacia arriba
            const arriba = (beta > -120 && beta < 120);

            // O si está con la pantalla hacia abajo
            const abajo = (beta <= -150 || beta >= 150);

            // Estado actual: true si la pantalla está visible (face up), false si está boca abajo
            const estadoActual = abajo ? false : arriba;

            // Solo emitimos si el estado cambió respecto al anterior
            if (estadoActual !== ultimoEstado) {
                socket.emit("posicion_pantalla", estadoActual); // true si visible, false si no
                ultimoEstado = estadoActual; // Guardamos el nuevo estado
            }
        }, { passive: true });
    } else {
        // Si no se soporta DeviceOrientation, asumimos que la pantalla está visible
        socket.emit("posicion_pantalla", true);
    }
});
