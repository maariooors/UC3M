// Esperamos a que el DOM esté completamente cargado antes de ejecutar el código
document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Conectamos con el servidor vía socket.io

    // Variables para guardar la distancia entre dos dedos al inicio y al final del gesto
    let distanciaInicial = 0;
    let distanciaFinal = 0;

    // Umbral de detección de zoom
    const umbral = 0.2;

    // Función auxiliar para calcular la distancia entre dos toques
    function distancia(touch1, touch2) {
        const dx = touch2.clientX - touch1.clientX;
        const dy = touch2.clientY - touch1.clientY;
        return Math.sqrt(dx * dx + dy * dy); // Usamos el teorema de Pitágoras
    }

    // Cuando el usuario pone los dedos en la pantalla
    document.addEventListener('touchstart', (e) => {
        // Solo nos interesa si hay exactamente dos dedos en contacto
        if (e.touches.length === 2) {
            distanciaInicial = distancia(e.touches[0], e.touches[1]);
            distanciaFinal = distanciaInicial;
            console.log(`Inicio - Distancia: ${distanciaInicial.toFixed(2)}px`);
        }
    }, { passive: true });

    // Mientras el usuario mueve los dedos
    document.addEventListener('touchmove', (e) => {
        if (e.touches.length === 2) {
            e.preventDefault(); // Evitamos zoom del navegador o scroll
            distanciaFinal = distancia(e.touches[0], e.touches[1]);
        }
    }, { passive: false });

    // Cuando se levantan los dedos
    document.addEventListener('touchend', (e) => {
        // Solo actuamos si teníamos una distancia inicial registrada
        if (distanciaInicial > 0) {
            // Calculamos el cambio proporcional de distancia entre el inicio y el final
            const cambioPorcentual = Math.abs(distanciaFinal - distanciaInicial) / distanciaInicial;

            console.log(`Final - Inicial: ${distanciaInicial.toFixed(2)}px | Final: ${distanciaFinal.toFixed(2)}px | Cambio: ${(cambioPorcentual * 100).toFixed(1)}%`);

            // Si ese cambio es mayor al umbral, consideramos que fue un gesto de zoom
            if (cambioPorcentual >= umbral) {
                const zoom = distanciaFinal > distanciaInicial; // Determinamos si fue zoom in o zoom out
                console.log(`Enviando al servidor: ${zoom}`);

                // Enviamos el tipo de gesto al servidor
                socket.emit('zoom_in_out', zoom);

            }

            // Reseteamos la distancia inicial
            distanciaInicial = 0;
        }
    }, { passive: true });
});
