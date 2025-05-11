// Esperamos a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // Conexión con el servidor
    const statusDisplay = document.getElementById('statusDisplay'); // Elemento donde mostramos el estado al usuario
    const startBtn = document.getElementById('startBtn'); // Botón para activar/desactivar el puntero

    // Variables para calibrar el dispositivo (posición inicial)
    let calibrado = false;
    let alphaDefecto = 0;
    let betaDefecto = 0;
    let siguiendo = false;

    // Coordenadas actuales del puntero
    let xActual = 0;
    let yActual = 0;

    // Detección de doble tap (para simular clic)
    let ultimoTap = 0;
    const retrasoDobleTap = 500; // Tiempo máximo entre taps para que se considere doble

    // Función para comenzar el seguimiento del puntero
    function empezarSeguir() {
        window.addEventListener('deviceorientation', handleOrientation); // Empezamos a escuchar la orientación
        startBtn.disabled = true;
        siguiendo = true;
        statusDisplay.textContent = 'Estado: Puntero activo. Por favor calibre apuntando a la pantalla.';
        socket.emit('puntero_estado', { activo: true }); // Notificamos al servidor que el puntero está activo
    }

    // Evento al tocar el botón para iniciar o detener el puntero
    startBtn.addEventListener('touchstart', () => {
        if (!siguiendo) {
            // En iOS hay que pedir permisos explícitos para usar los sensores
            if (typeof DeviceOrientationEvent.requestPermission === 'function') {
                DeviceOrientationEvent.requestPermission()
                    .then(permissionState => {
                        if (permissionState === 'granted') {
                            empezarSeguir();
                        } else {
                            statusDisplay.textContent = 'Estado: Permiso denegado para acceder al puntero.';
                        }
                    })
                    .catch(console.error);
            } else {
                // En otros navegadores arrancamos directamente
                empezarSeguir();
            }

            // Comenzamos calibración
            statusDisplay.textContent = 'Estado: Calibrando... Mantenga el dispositivo apuntando a la pantalla.';
            calibrado = false;

            setTimeout(() => {
                calibrado = true; // Después de 1 segundo asumimos que ya está calibrado
                statusDisplay.textContent = 'Estado: ¡Calibrado! Ya puede usar el puntero.';
            }, 1000);

        } else {
            // Si ya estaba activo, detenemos el seguimiento
            window.removeEventListener('deviceorientation', handleOrientation);
            startBtn.disabled = false;
            siguiendo = false;
            statusDisplay.textContent = 'Estado: Puntero detenido';

            socket.emit('eliminar_puntero'); // Le decimos al servidor que lo elimine
            socket.emit('puntero_estado', { activo: false });
        }
    });

    // Doble tap para generar un "click"
    document.addEventListener('touchstart', (event) => {
        if (!siguiendo) return;

        const horaActual = new Date().getTime();
        const intervaloTap = horaActual - ultimoTap;

        if (intervaloTap < retrasoDobleTap && intervaloTap > 0) {
            event.preventDefault(); // Evitamos zoom o comportamientos por defecto

            statusDisplay.textContent = '¡Click!';
            setTimeout(() => {
                if (siguiendo) {
                    statusDisplay.textContent = 'Estado: Calibrado! Ya puede dibujar moviendo el dispositivo y hacer doble tap para hacer click';
                }
            }, 500);

            socket.emit('clickPuntero'); // Avisamos al servidor que hubo un click
        }

        ultimoTap = horaActual; // Actualizamos la hora del último tap
    });

    // Función para manejar la orientación del dispositivo
    function handleOrientation(event) {
        if (!siguiendo) return; // Si no estamos rastreando, ignoramos

        // Obtenemos los ángulos de orientación
        const alpha = event.alpha || 0; // Rotación en el eje Z
        const beta = event.beta || 0;   // Inclinación adelante/atrás

        // Si no está calibrado, usamos esta orientación como referencia inicial
        if (!calibrado) {
            alphaDefecto = alpha;
            betaDefecto = beta;
            return;
        }

        // Calculamos la diferencia desde la posición base (calibrada)
        let alphaDiff = alpha - alphaDefecto;

        // Manejamos el caso especial de que alpha pase de 360 a 0 (o al revés)
        if (alphaDiff > 180) alphaDiff -= 360;
        if (alphaDiff < -180) alphaDiff += 360;

        const betaDiff = beta - betaDefecto;

        // Factor de sensibilidad (se puede ajustar para hacerlo más o menos sensible)
        const sensibilidad = 1;

        // Calculamos la posición "virtual" del puntero
        xActual = alphaDiff * sensibilidad;
        yActual = betaDiff * sensibilidad;

        // Enviamos la posición al servidor para mover el puntero allá
        socket.emit('puntero', {
            roll: xActual,  // Movimiento horizontal (izq-der)
            pitch: yActual  // Movimiento vertical (arriba-abajo)
        });
    }
});
