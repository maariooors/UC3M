// Importamos módulos necesarios para el servidor y manejo de archivos
const path = require("path");
const http = require("http");
const express = require("express");
const socketIo = require("socket.io");
const fs = require('fs');

const app = express(); // Inicializamos Express para manejar peticiones HTTP
const server = http.createServer(app); // Creamos un servidor HTTP con Express como manejador
const io = socketIo(server); // Inicializamos Socket.IO para comunicación en tiempo real con clientes
const PORT = 3000; // Puerto donde correrá nuestro servidor

// Middleware para servir archivos estáticos desde la carpeta "public"
app.use(express.static(path.join(__dirname, "public")));

// Definimos rutas para servir páginas específicas
app.get("/movil", (req, res) => {
	res.sendFile(path.join(__dirname, "public", "/views/movil.html")); // Página para móvil
});

app.get("/calendario", (req, res) => {
	res.sendFile(path.join(__dirname, "public", "/views/calendario.html")); // Página calendario
});

// Configuración de eventos para conexiones Socket.IO
io.on("connection", (socket) => {
	console.log(`Cliente conectado: ${socket.id}`);

	// Escuchamos evento de posición del móvil (boca arriba o boca abajo)
    socket.on('posicion_pantalla', isFaceUp => {
		// Emitimos a todos los clientes la acción para actualizar la pantalla
		io.emit('accion_posicion_pantalla', isFaceUp);
        console.log('Orientación:', isFaceUp ? 'Boca arriba (true)' : 'Boca abajo (false)');
    });

    // Escuchamos eventos de zoom (in/out) desde el cliente móvil
    socket.on('zoom_in_out', isZoomIn => {
        io.emit('accion_zoom_in_out', isZoomIn);
        console.log(`[ZOOM] ${isZoomIn ? 'IN (true)' : 'OUT (false)'}`);
    });

    socket.on('scroll', data => {
        io.emit('mover_pantalla', data);
    });

    // Escuchamos eventos de volumen (subir/bajar)
    socket.on('volumen', isVolumeUp => {
        io.emit('accion_volumen', isVolumeUp);
        console.log('Acción de volumen:', isVolumeUp);
    });

	// Evento para detectar rotación del móvil (izquierda/derecha)
	socket.on('rotacion_movil', direction => {
		io.emit('rotacion_movil', direction);
		console.log("Rotación Movil: ", direction);
	});

    // Recibimos datos del puntero y los emitimos para todos
    socket.on('puntero', data => {
        io.emit('puntero', data);
    });

    // Evento de click enviado desde el móvil
    socket.on('clickPuntero', () => {
        io.emit('clickPuntero');
    });

    // Estado del puntero activo o no
    socket.on('puntero_estado', data => {
        io.emit('puntero_estado', data);
    });

    // Evento para eliminar el puntero de la pantalla
    socket.on('eliminar_puntero', () => {
        io.emit('eliminar_puntero');
    });

    // Solicitud para iniciar reconocimiento de voz desde el cliente
    socket.on('iniciar_voz', (data) => {
        console.log('Cliente ha solicitado iniciar el reconocimiento de voz', data);
        io.emit('procesar_voz', { mensaje: "Iniciar procesamiento de voz y cambiar horario" });
    });

    // Recepción de imagen capturada desde el cliente (en base64)
    socket.on('imagen_capturada', (photoData) => {
        console.log(`Received photo: ${photoData.filename}`);
        
        // Convertimos la imagen base64 a buffer binario
        const imageBuffer = Buffer.from(photoData.image, 'base64');
        
        // Definimos ruta para guardar imágenes
        const publicImgDir = path.join(__dirname, 'public', 'img');
        
        // Verificamos que la carpeta exista, si no la creamos
        if (!fs.existsSync(publicImgDir)) {
            fs.mkdirSync(publicImgDir, { recursive: true });
        }
        
        // Función para generar nombre único de archivo con formato "nombre-1.jpg", "nombre-2.jpg", etc.
        const generateUniqueFilename = (nombre, extension) => {
            let counter = 1;
            let newName = `${nombre}-${counter}`; // Comenzamos con -1
            
            // Incrementamos el contador mientras exista un archivo con ese nombre
            while (fs.existsSync(path.join(publicImgDir, `${newName}${extension}`))) {
                counter++;
                newName = `${nombre}-${counter}`;
            }
            
            return `${newName}${extension}`;
        };
        
        // Obtenemos nombre base y extensión del archivo enviado
        const ruta = path.parse(photoData.filename);
        const nombre = ruta.name;
        const extension = ruta.ext;
        
        // Generamos un nombre único para la nueva foto
        const nombreArchivo = generateUniqueFilename(nombre, extension);
        
        // Guardamos la imagen en el disco
        fs.writeFile(path.join(publicImgDir, nombreArchivo), imageBuffer, (err) => {
            if (err) {
                console.error('Error saving photo:', err);
            } else {
                console.log(`Photo saved: ${nombreArchivo}`);
            }
        });
    });

    // Evento para verificar fotos existentes para un día y mes específico
    socket.on('verificarFotos', (data) => {
        const { dia, mes } = data;
        
        // Buscamos fotos que coincidan con el día y mes
        const fotos = buscarFotos(dia, mes);
        
        // Enviamos la lista de fotos encontradas solo al cliente que solicitó
        socket.emit('fotosDia', { fotos });
    });
  

    // Repetimos el evento desconexión para asegurar su manejo
    socket.on("disconnect", () => {
		console.log(`Cliente desconectado: ${socket.id}`);
	});


});

// Función que busca fotos guardadas en el servidor para un día y mes dados
function buscarFotos(dia, mes) {
    const fotosDir = path.join(__dirname, 'public', 'img');
    const prefijo = `${dia}_${mes}`; // Prefijo esperado en el nombre de archivo, p.ej "15_4" para 15 de abril
    
    try {
        // Leemos todos los archivos del directorio de imágenes
        const archivos = fs.readdirSync(fotosDir);
        
        // Filtramos solo las imágenes que tengan el prefijo del día y mes
        const fotos = archivos.filter(archivo => {
            return archivo.startsWith(prefijo) && 
                   (archivo.endsWith('.jpg') || archivo.endsWith('.jpeg') || 
                    archivo.endsWith('.png') || archivo.endsWith('.gif'));
        });
        
        // Devolvemos las rutas relativas para que puedan ser accedidas por el cliente
        return fotos.map(foto => `/img/${foto}`);
    } catch (error) {
        console.error('Error al buscar fotos:', error);
        return [];
    }
}

// Arrancamos el servidor escuchando en el puerto definido
server.listen(PORT, () => {
	console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
});

// Manejamos posibles errores del servidor
server.on("error", (error) => {
	console.error("Error en el servidor:", error);
});
