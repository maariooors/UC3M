window.socket = io(); 
// Inicializamos la conexión con el servidor usando socket.io y la guardamos en window para que esté disponible globalmente

document.addEventListener('DOMContentLoaded', () => {
    // Esperamos a que el DOM esté listo para ejecutar el código

    // Obtenemos el nombre de la página actual desde la URL, para usarlo en logs y lógica
    const paginaActual = window.location.pathname.split('/').pop().split('.')[0] || 'index';
    console.log(`Current page: ${paginaActual}`);
    
    // Variable para controlar si el puntero está activo o no
    let punteroActivo = false;

    // Escuchamos el evento 'puntero_estado' desde el servidor para actualizar si el puntero está activo
    socket.on('puntero_estado', data => {
        console.log('[puntero_estado] recibido:', data);
        punteroActivo = data.activo;
    });

    // Seleccionamos todos los elementos de audio que haya en la página
    const elementosAudio = document.querySelectorAll('audio');
    // Elementos del DOM para mostrar el indicador de volumen y su valor
    const indicadorVolumen = document.getElementById('indicador-volumen');
    const valorVolumen = document.getElementById('valor-volumen');
    
    // Guardamos el volumen en una variable global para controlar su valor
    let volumen = 0.5; // Valor inicial

    // Función para mostrar el indicador de volumen y ocultarlo tras 2 segundos
    function mostrarIndicadorVolumen() {
        indicadorVolumen.style.display = 'block';  // Lo mostramos
        clearTimeout(indicadorVolumen.timeout);   // Limpiamos cualquier timeout previo
        indicadorVolumen.timeout = setTimeout(() => {
            indicadorVolumen.style.display = 'none'; // Lo ocultamos después de 2s
        }, 2000);
    }

    // Escuchamos cambios en la posición de la pantalla desde el servidor
    socket.on('accion_posicion_pantalla', posicion => {
        let pantallaNegra = document.getElementById("pantalla-negra");
        if (!pantallaNegra) return; // Si no hay elemento en esta página, salimos

        // Si posicion es true ocultamos la pantalla negra, si es false la mostramos
        if (posicion == true){
            pantallaNegra.classList.add("hidden");
        } else if (posicion == false) {
            pantallaNegra.classList.remove("hidden");
        }
    });

    // Escuchamos comandos para cambiar el volumen
    socket.on('accion_volumen', cambio_volumen => {
        console.log(cambio_volumen);
        
        if (cambio_volumen == true) {
            // Si el comando es true, subimos el volumen 0.1 hasta un máximo de 1
            volumen = Math.min(volumen + 0.1, 1);
            mostrarIndicadorVolumen();
        } else if (cambio_volumen == false) {
            // Si el comando es false, bajamos el volumen 0.1 hasta un mínimo de 0
            volumen = Math.max(volumen - 0.1, 0);
            mostrarIndicadorVolumen();
        }
        
        // Aplicamos el nuevo volumen a todos los elementos de audio en la página
        elementosAudio.forEach(audio => {
            audio.volume = volumen;
        });
        
        // Actualizamos el texto que muestra el porcentaje de volumen
        if (valorVolumen) {
            valorVolumen.textContent = Math.round(volumen * 100);
        }
    });

    // Código para controlar el puntero en pantalla
    
    // Obtenemos el canvas donde dibujaremos el puntero
    const canvas = document.getElementById('canvas');
    if (!canvas) {
        console.error('Canvas element not found');
        return;  // Si no hay canvas, no continuamos con el puntero
    }
    
    // Obtenemos el contexto 2D del canvas para dibujar
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Could not get canvas context');
        return;
    }

    console.log(`[${paginaActual}] Canvas:`, canvas);
    console.log(`[${paginaActual}] Contexto:`, ctx);

    // Dibujamos un círculo verde de prueba para verificar que el canvas funciona
    ctx.beginPath();
    ctx.arc(50, 50, 10, 0, Math.PI * 2);
    ctx.fillStyle = 'green';
    ctx.fill();
    console.log(`[${paginaActual}] Test circle drawn`);

    // Cargamos la imagen que usaremos para representar el puntero
    const punteroImg = new Image();
    punteroImg.src = 'https://i.postimg.cc/nL36QNZv/mano-Select.png';
    const pointerSize = 45;  // Tamaño del puntero
    let imagenCargada = false;
    punteroImg.onload = () => { 
        imagenCargada = true;  // Marcamos que la imagen ya cargó
        console.log(`[${paginaActual}] Pointer image loaded`);
    };

    // Función para redimensionar el canvas al tamaño de la ventana
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        console.log(`[${paginaActual}] Canvas resized to ${canvas.width}x${canvas.height}`);
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();  // Llamamos una vez al inicio para ajustar tamaño

    // Variables para guardar la última posición conocida del puntero
    let utlimaX = canvas.width / 2, utlimaY = canvas.height / 2;
    let punteroInicializado = false;  // Control para saber si ya iniciamos la posición del puntero

    // Escuchamos evento para eliminar el puntero (limpiar canvas)
    socket.on('eliminar_puntero', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpiamos todo el canvas
        punteroInicializado = false;  // Reiniciamos el estado
        console.log(`[${paginaActual}] Puntero eliminado`);
    });

    // Evento que recibe la posición del puntero y lo dibuja en el canvas
    socket.on('puntero', (data) => {
        console.log(`[${paginaActual}] [PUNTERO] Evento recibido con datos:`, data);
        if (!punteroActivo) return;  // Si el puntero no está activo, no dibujamos
        
        // Limpiamos el canvas antes de dibujar para evitar trazos anteriores
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Definimos el rango máximo de movimiento para girar y pitch
        const rangoGirar = 30;
        const rangoPitch = 30;

        // Calculamos la nueva posición en X y Y del puntero basándonos en roll y pitch recibidos
        // Ajustamos para centrar y limitar dentro del tamaño del canvas
        const newX = canvas.width / 2 - (data.roll / rangoGirar) * canvas.width / 2;
        const newY = canvas.height / 2 - (data.pitch / rangoPitch) * canvas.height / 2;

        // Limitamos las coordenadas para que no salgan fuera del canvas
        const boundedX = Math.max(0, Math.min(canvas.width, newX));
        const boundedY = Math.max(0, Math.min(canvas.height, newY));

        if (!punteroInicializado) {
            // Si no hemos inicializado, asignamos la posición actual y marcamos que sí
            utlimaX = boundedX;
            utlimaY = boundedY;
            punteroInicializado = true;
        } else {
            // Si la imagen del puntero está cargada, dibujamos la imagen centrada en la posición
            if (imagenCargada) {
                console.log(`[${paginaActual}] [PUNTERO] Dibujando imagen en ${boundedX}, ${boundedY}`);
                ctx.drawImage(punteroImg, boundedX - pointerSize / 2, boundedY - pointerSize / 2, pointerSize, pointerSize);
            } else {
                // Si no, dibujamos un círculo rojo como fallback
                console.log(`[${paginaActual}] [PUNTERO] Dibujando círculo en ${boundedX}, ${boundedY}`);
                ctx.beginPath();
                ctx.arc(boundedX, boundedY, 10, 0, Math.PI * 2);
                ctx.fillStyle = 'red';
                ctx.fill();
            }

            // Guardamos la última posición del puntero para usarla en clicks
            utlimaX = boundedX;
            utlimaY = boundedY;
        }
    });
    // Código para el puntero

    // Escuchamos evento de click que venga desde el móvil para simular un click en la posición del puntero
    socket.on('clickPuntero', () => {
        const x = utlimaX;
        const y = utlimaY;
    
        // Obtenemos el elemento del DOM que esté en la posición del puntero
        const element = document.elementFromPoint(x, y);
    
        if (element) {
            element.click();  // Simulamos un click en ese elemento
        }
        
        console.log(`[${paginaActual}] Click detected at ${x}, ${y}`);
    });
});
