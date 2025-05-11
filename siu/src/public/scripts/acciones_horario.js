document.addEventListener('DOMContentLoaded', () => {

    socket.on('accion_zoom_in_out', zoom => {
        console.log(zoom);
        // Si recibimos un falso, volvemos a la página anterior en el historial
        if (zoom == false) {
            window.history.go(-1);
        }
    });

    socket.on('mover_pantalla', (data) => {
        console.log("Recibido mover_pantalla a:", data.y);
        window.scrollTo({ top: data.y, behavior: 'smooth' });
    });

    const style = document.createElement('style');
style.textContent = `
  .toast-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 12px 20px;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
    max-width: 300px;
    text-align: center;
  }

  .toast-notification.show {
    opacity: 1;
  }
`;
document.head.appendChild(style);

// Función para mostrar la notificación
function mostrat_popup(message, duration = 3000) {
  // Crear el elemento de notificación
  const toast = document.createElement('div');
  toast.className = 'toast-notification';
  toast.textContent = message;
  document.body.appendChild(toast);
  
  // Forzar un reflow para que la transición funcione correctamente
  setTimeout(() => {
    toast.classList.add('show');
  }, 10);
  
  // Configurar el temporizador para ocultar y eliminar la notificación
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300); // Esperar a que termine la transición de opacidad
  }, duration);
}

  socket.on('procesar_voz', (data) => {
        console.log(data.mensaje);  // Nos indica que debemos iniciar reconocimiento de voz
        empezarReconocimiento();
    });

    // Función para iniciar el reconocimiento de voz usando la API Web Speech
    function empezarReconocimiento() {
        // Usamos la API de reconocimiento de voz, verificando compatibilidad entre navegadores
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!window.SpeechRecognition) {
            console.error("El navegador no soporta reconocimiento de voz");
            return;
        }
        
        const reconocimiento = new SpeechRecognition();
        reconocimiento.lang = "es-ES"; // Configuramos idioma español de España
        reconocimiento.start();

        // Cuando se detecta un resultado
        reconocimiento.onresult = (event) => {
            const texto = event.results[0][0].transcript.toLowerCase();
            console.log("Comando detectado: ", texto);
            // Enviamos el texto para ser procesado
            procesarNotaPorVoz(texto);
        };

        // Capturamos posibles errores en el reconocimiento
        reconocimiento.onerror = (event) => {
            console.error("Error en el reconocimiento:", event.error);
        };
    }

    // Función que procesa el texto reconocido para extraer información
    function procesarNotaPorVoz(texto) {
        console.log("Texto recibido para procesar: ", texto);

        // Regex para extraer hora, actividad y nota con formato tipo:
        // "nota a las 12:30 actividad descripción"
        const regex = /nota.*?(?:a las )?(\d{1,2}:\d{2})\s+(.+?)\s+(.+)/i;
        const match = texto.match(regex);

        // Si no cumple el formato esperado, avisamos y no hacemos nada
        if (!match) {
  
            mostrat_popup("Formato no reconocido", 3000);
            console.log("Formato no reconocido");
            return;
        }

        // Normalizamos la hora para asegurar formato correcto
        let hora = match[1];
        const [horas, minutos] = hora.split(':');
        hora = `${parseInt(horas)}:${minutos}`;

        // Actividad y nota extraídas
        let actividadNombre = match[2].trim();
        actividadNombre = actividadNombre.charAt(0).toUpperCase() + actividadNombre.slice(1);
        const notaTexto = match[3].trim();

        console.log(`Hora: ${hora}, Actividad: ${actividadNombre}, Nota: ${notaTexto}`);

        
        // Ahora buscamos la actividad y la actualizamos en el horario
        actualizarActividad(hora, actividadNombre, notaTexto);
    }
        function actualizarActividad(hora, actividadNombre, notaTexto) {
            // Buscar la actividad en el HTML y actualizarla
            const actividades = document.querySelectorAll('.actividad');
    
            actividades.forEach(actividad => {
                const horaActividad = actividad.querySelector('.hora').textContent;
    
                // Si la hora de la actividad coincide, actualizamos la actividad
                if (horaActividad === hora) {
                    const nombreActividad = actividad.querySelector('.nombre');
                    nombreActividad.textContent = `${actividadNombre}: ${notaTexto}`;
                    console.log(`Actividad actualizada: ${nombreActividad.textContent}`);
                }
            });
        }
    

    // Iniciamos la detección de manos cuando el DOM esté listo
    inicializarMediaPipe();
});

// Constantes para MediaPipe manos
const PUNTAS_DEDOS = [4, 8, 12, 16, 20]; // Pulgar, Índice, Medio, Anular, Meñique
const BASE_DEDOS = [2, 5, 9, 13, 17]; // Articulaciones base para cada dedo

// Referencias a elementos HTML
const videoElement = document.getElementById('video');
const canvasElement = document.getElementById('output-canvas');
const canvasCtx = canvasElement ? canvasElement.getContext('2d') : null;
const statusElement = document.getElementById('status');
const countdownElement = document.getElementById('countdown');

// Variables globales
let camara = null;
let manosDetector = null;
let corriendo = false;
let tiempoManoCerrada = null;
let contadorBajando = false;
let intervaloCuenta = null;
let cuentaActivada = false;
let fotoCanvas = document.createElement('canvas');
let fotoCtx = fotoCanvas.getContext('2d');

// Inicialización de MediaPipe
function inicializarMediaPipe() {
    // Verificamos que la librería esté cargada correctamente
    if (!window.Hands) {
        console.error("MediaPipe Hands no está cargado correctamente");
        if (statusElement) statusElement.textContent = "Error: MediaPipe no cargado.";
        
        // Intentamos recargar la librería
        const script = document.createElement('script');
        script.src = "https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js";
        script.onload = () => {
            console.log("MediaPipe Hands recargado. Intentando inicializar...");
            inicializarDetectorManos();
        };
        document.head.appendChild(script);
        return;
    }
    
    inicializarDetectorManos();
}

// Inicializa el detector de manos de MediaPipe
function inicializarDetectorManos() {
    try {
        manosDetector = new Hands({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
            }
        });

        // Configuramos opciones
        manosDetector.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        // Definimos la función para procesar resultados
        manosDetector.onResults(procesarResultadosManos);

        // Preparamos canvas para fotos
        fotoCanvas.width = 640;
        fotoCanvas.height = 480;
        
        // Iniciamos la cámara
        iniciarCamara();
        
        // if (statusElement) statusElement.textContent = "MediaPipe inicializado correctamente";
    } catch (error) {
        console.error("Error al inicializar MediaPipe Hands:", error);
        if (statusElement) statusElement.textContent = "Error al inicializar MediaPipe: " + error.message;
    }
}

// Función para determinar si un dedo está extendido
function dedoExtendido(marcasMano, tipIdx, baseIdx) {
    // Para el pulgar la lógica es diferente por su orientación
    if (tipIdx === 4) {
        const thumbTip = marcasMano[tipIdx];
        const thumbCmc = marcasMano[1];
        // El pulgar está extendido si la punta está a la izquierda respecto a la base
        return thumbTip.x < thumbCmc.x;
    }
    
    // Para los demás dedos, comparamos verticalmente
    const tipY = marcasMano[tipIdx].y;
    const baseY = marcasMano[baseIdx].y;
    return tipY < baseY;
}

// Función para determinar si la mano está abierta o cerrada
function estadoMano(marcasMano) {
    let dedosExtendidos = 0;
    
    for (let i = 0; i < PUNTAS_DEDOS.length; i++) {
        if (dedoExtendido(marcasMano, PUNTAS_DEDOS[i], BASE_DEDOS[i])) {
            dedosExtendidos++;
        }
    }
    
    // Consideramos mano abierta si hay 3 o más dedos extendidos
    return dedosExtendidos >= 3 ? 'abierta' : 'cerrada';
}

// Función para iniciar la cuenta regresiva
function empezarContador() {
    if (contadorBajando) return;

    contadorBajando = true;
    cuentaActivada = true;
    let secondsLeft = 3;
    countdownElement.textContent = secondsLeft;

    intervaloCuenta = setInterval(() => {
        secondsLeft--;
        countdownElement.textContent = secondsLeft;

        if (secondsLeft <= 0) {
            clearInterval(intervaloCuenta);
            hacerFoto();
            contadorBajando = false;
            cuentaActivada = false;
            countdownElement.textContent = '';
        }
    }, 1000);
}

// Función para capturar foto
function hacerFoto() {
    if (!corriendo) {
        console.error("Cámara no iniciada");
        return;
    }
    
    // Dibujamos el video en el canvas (invertido horizontalmente)
    fotoCtx.save();
    fotoCtx.scale(-1, 1);
    fotoCtx.drawImage(videoElement, -fotoCanvas.width, 0, fotoCanvas.width, fotoCanvas.height);
    fotoCtx.restore();
    
    // Obtenemos día y mes desde parámetros URL
    const urlParams = new URLSearchParams(window.location.search);
    const dia = urlParams.get('dia') || new Date().getDate();
    const mes = urlParams.get('mes') || new Date().getMonth() + 1;
    
    const nombreFichero = `${dia}_${mes}.jpg`;

    // Convertimos la imagen a base64
    const dataUrl = fotoCanvas.toDataURL('image/jpeg');
    enviarFotoAlServidor(dataUrl, nombreFichero);

    // Efecto visual de flash
    mostrarFlash();
}

// Muestra un flash visual cuando se toma una foto
function mostrarFlash() {
    const flash = document.createElement('div');
    flash.style.position = 'fixed';
    flash.style.top = '0';
    flash.style.left = '0';
    flash.style.width = '100%';
    flash.style.height = '100%';
    flash.style.backgroundColor = 'white';
    flash.style.opacity = '0.7';
    flash.style.zIndex = '1000';
    flash.style.pointerEvents = 'none';
    document.body.appendChild(flash);

    // Quitamos el flash después de 150ms
    setTimeout(() => {
        document.body.removeChild(flash);
    }, 150);
}

// Enviar la foto al servidor
function enviarFotoAlServidor(dataUrl, nombreFichero) {
    // Quitamos el prefijo
    const base64Data = dataUrl.replace(/^data:image\/jpeg;base64,/, '');

    // Creamos el objeto con datos
    const fotoInfo = {
        image: base64Data,
        filename: nombreFichero,
        timestamp: new Date().toISOString()
    };

    // Enviamos al servidor
    socket.emit('imagen_capturada', fotoInfo);
    console.log("Foto enviada al servidor:", nombreFichero);

    // Actualizamos el estado en la UI
    if (statusElement) {
        const prevStatus = statusElement.textContent;
        // statusElement.textContent = "Foto enviada al servidor";

        setTimeout(() => {
            statusElement.textContent = prevStatus;
        }, 2000);
    }
}

// Procesa los resultados de detección de manos
function procesarResultadosManos(results) {
    if (!canvasCtx || !results.image) return;

    // Limpiamos el canvas y dibujamos la imagen
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

    let manoCerrada = false;

    // Si detectamos al menos una mano y no hay cuenta regresiva activa
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const marcasMano = results.multiHandLandmarks[0];
        const estado = estadoMano(marcasMano);
        
        if (estado === 'cerrada') {
            manoCerrada = true;
        }

        const tiempoActual = Date.now();

        // Si la mano está cerrada, manejamos la cuenta regresiva
        if (manoCerrada) {
            if (tiempoManoCerrada === null) {
                tiempoManoCerrada = tiempoActual;
            } else if (!contadorBajando && tiempoActual - tiempoManoCerrada > 500) {
                empezarContador();
            }
        } else {
            tiempoManoCerrada = null;
        }
        
        // Dibujamos las marcas de la mano
        drawConnectors(canvasCtx, marcasMano, HAND_CONNECTIONS, { color: '#00FF00', lineWidth: 4 });
        drawLandmarks(canvasCtx, marcasMano, { color: '#FF0000', lineWidth: 2 });
    } else {
        tiempoManoCerrada = null;
    }

    canvasCtx.restore();
}

// Función para iniciar la cámara
function iniciarCamara() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("La cámara no está disponible en este navegador");
        return;
    }

    // Usamos la cámara frontal si está disponible
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
        .then((stream) => {
            videoElement.srcObject = stream;
            videoElement.play();

            camara = {
                stream: stream,
                stop: () => {
                    stream.getTracks().forEach(track => track.stop());
                }
            };

            corriendo = true;

            // Enviamos cada frame a MediaPipe
            const procesarFrameVideo = async () => {
                if (!corriendo) return;

                await manosDetector.send({ image: videoElement });
                requestAnimationFrame(procesarFrameVideo);
            };

            procesarFrameVideo();
        })
        .catch(err => {
            console.error("Error accediendo a la cámara:", err);
            if (statusElement) statusElement.textContent = "Error accediendo a la cámara: " + err.message;
        });
}
