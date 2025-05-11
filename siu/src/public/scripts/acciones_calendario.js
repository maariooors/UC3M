const socket = window.socket; 
// Reutilizamos la conexión socket.io que ya creamos antes.

document.addEventListener('DOMContentLoaded', () => {
    // Variables para controlar el estado de navegación del calendario
    let mesActual = 1;      // Mes actual mostrado, empezamos en enero (1)
    let contadorIzquierda = 0; // Contador de giros a la izquierda detectados
    let contadorDerecha = 0;   // Contador de giros a la derecha detectados
    const girosMinimos = 7;    // Número mínimo de giros seguidos para considerar una acción
    let cooldown = false;      // Control para evitar que los giros se detecten demasiado rápido

    // Controlamos si el puntero está activo para evitar conflictos
    let punteroActivo = false;

    // Escuchamos si el servidor indica que el puntero está activo o no
    socket.on('puntero_estado', data => {
        punteroActivo = data.activo;
    });

    // Escuchamos eventos para zoom, si nos indican zoom-in/zoom-out hacemos avance en el historial
    socket.on('accion_zoom_in_out', zoom => {
        if (zoom == true) {
            // Simulamos ir hacia adelante en la historia del navegador
            window.history.forward();
        }
    });

    // Evento que detecta la rotación del móvil, para cambiar el mes con giros
    socket.on('rotacion_movil', direccion => {
        if (punteroActivo) return;   // Si el puntero está activo, ignoramos giros para evitar conflicto
        if (cooldown) return;        // Si estamos en cooldown, ignoramos para no procesar rápido giros seguidos
		
		console.log(`Giro detectado: ${direccion}`);
	
		// Si la dirección es izquierda, aumentamos el contador izquierdo y reseteamos el derecho
		if (direccion === 'left') {
			contadorIzquierda++;
			contadorDerecha = 0;
		} else if (direccion === 'right') {
			// Si es derecha, aumentamos el contador derecho y reseteamos el izquierdo
			contadorDerecha++;
			contadorIzquierda = 0;
		}

        // Si alguno de los contadores llega o supera girosMinimos (7)
        if (contadorIzquierda >= girosMinimos || contadorDerecha >= girosMinimos) {
			const direccion = contadorIzquierda >= girosMinimos ? 'left' : 'right';
			
            if (direccion === 'left') {
                // Si el giro fue hacia la izquierda, vamos al mes anterior
                // Si estamos en enero (1), regresamos a diciembre (12) para que sea circular
                mesActual = mesActual > 1 ? mesActual - 1 : 12;
            } else if (direccion === 'right') {
                // Si el giro fue hacia la derecha, vamos al mes siguiente
                // Si estamos en diciembre (12), volvemos a enero (1) para que sea circular
                mesActual = mesActual < 12 ? mesActual + 1 : 1;
            }
            
            // Actualizamos el calendario con el nuevo mes seleccionado
            actualizarCalendario(mesActual);
			
			// Reiniciamos los contadores y activamos cooldown para evitar movimientos muy rápidos
			contadorIzquierda = contadorDerecha = 0;
			cooldown = true;
			setTimeout(() => cooldown = false, 1000);  // Esperamos 1 segundo antes de aceptar otro giro
		}

    });

    // Función que actualiza el calendario y el título según el mes actual
    function actualizarCalendario(month) {
        // Cambiamos el título del mes (usamos array 'meses' definido fuera, con nombres de meses)
        document.getElementById("month-title").innerText = meses[month - 1] + " 2025";
        // Cambiamos el contenido del calendario (array 'calendarios' con contenido HTML por mes)
        document.getElementById("calendar-container").innerHTML = calendarios[month];
    }
    
    // Inicializamos el calendario mostrando el mes 1 (enero)
    actualizarCalendario(mesActual);
});
