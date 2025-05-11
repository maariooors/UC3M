// Esperamos a que todo el contenido del DOM esté cargado antes de ejecutar nuestro script
document.addEventListener("DOMContentLoaded", () => {
    // Creamos una conexión con el servidor usando socket.io
    const socket = io();

    // Array para ir guardando la secuencia de gestos detectados
    let patronGestos = [];

    // Definimos el patrón que queremos detectar (izquierda, derecha, izquierda, derecha)
    const patronObjetivo = ['left', 'right', 'left', 'right'];

    // También definimos el patrón inverso por si queremos aceptarlo también
    const patronObjetivoInverso = ['right', 'left', 'right', 'left'];

    // Flag para evitar que se dispare múltiples veces seguidas el reconocimiento
    let cooldown = false;

    // Escuchamos el evento 'rotacion_movil' que recibimos desde el servidor
    socket.on('rotacion_movil', direction => {

        // Si estamos en cooldown, no procesamos más gestos
        if (cooldown) return;
        
        // Solo agregamos el nuevo gesto si es diferente del último (evita repeticiones consecutivas)
        if (patronGestos.length === 0 || patronGestos[patronGestos.length - 1] !== direction) {
            patronGestos.push(direction);
        }
        
        // Solo queremos guardar los últimos 4 gestos, así que eliminamos el primero si hay más de 4
        if (patronGestos.length > 4) {
            patronGestos.shift();
        }
        
        // Verificamos si el patrón actual coincide con el esperado o su versión inversa
        const esPatronObjetivo = arraysIguales(patronGestos, patronObjetivo);
        const esPatronObjetivoInverso = arraysIguales(patronGestos, patronObjetivoInverso);
        

        // Si hay coincidencia con alguno de los patrones, activamos el reconocimiento de voz
        if (esPatronObjetivo || esPatronObjetivoInverso) {

            // Enviamos al servidor una señal para iniciar el reconocimiento de voz
            socket.emit("iniciar_voz", { mensaje: "Iniciar reconocimiento de voz" });
            
            // Reseteamos el patrón y activamos cooldown para evitar múltiples activaciones
            patronGestos = [];
            cooldown = true;
            setTimeout(() => cooldown = false, 1000); // Esperamos 1 segundo antes de permitir otra detección
        }
    });

    // Función auxiliar para comparar si dos arrays son exactamente iguales
    function arraysIguales(arr1, arr2) {
        if (arr1.length !== arr2.length) return false;
        for (let i = 0; i < arr1.length; i++) {
            if (arr1[i] !== arr2[i]) return false;
        }
        return true;
    }
});
