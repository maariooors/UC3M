document.addEventListener('DOMContentLoaded', function() {
    const socket = io(); // Conexión con el servidor vía socket.io

    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        socket.emit('scroll', { y: scrollPosition });
    });


    const audioMeditacion = document.getElementById('audio-meditacion');
    
    // Obtenemos los parámetros de fecha desde la URL
    const urlParams = new URLSearchParams(window.location.search);
    const dia = parseInt(urlParams.get('dia'));
    const mes = parseInt(urlParams.get('mes'));
    const diaSemana = urlParams.get('diaSemana');
    
    // Nombres de meses y días de la semana
    const meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    const diasSemana = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
    
    // Creamos un objeto Date y determinar el día de la semana si no se especificó
    const fecha = new Date(2025, mes - 1, dia);
    const nombreDiaSemana = diaSemana || diasSemana[fecha.getDay()];
    const nombreMes = meses[mes - 1];
    
    // Mostramos la fecha completa en el encabezado
    document.getElementById('titulo-fecha').textContent = 
        `Día ${nombreDiaSemana} ${dia} de ${nombreMes}`;
    
    // Lista de posibles actividades diarias
    const actividadesPosibles = [
        { nombre: "Desayuno", musica: null },
        { nombre: "Trabajo", musica: null },
        { nombre: "Estudio", musica: "audio-estudio" },
        { nombre: "Almuerzo", musica: null },
        { nombre: "Reunión", musica: null },
        { nombre: "Descanso", musica: null },
        { nombre: "Lectura", musica: null },
        { nombre: "Cena", musica: null },
        { nombre: "Dormir", musica: null },
        { nombre: "Transporte", musica: "audio-transporte" },
        { nombre: "Compras", musica: null },
        { nombre: "Limpieza", musica: null },
        { nombre: "Proyectos", musica: null },
        { nombre: "Ocio", musica: null },
        { nombre: "Deporte", musica: null },
        { nombre: "Meditación", musica: "audio-meditacion" },
        { nombre: "Familia", musica: null },
        { nombre: "Amigos", musica: null }
    ];
    
    // Generamos número aleatorio entre 1 y 5
    function aleatorio1a5() {
        return Math.floor(Math.random() * 5) + 1;
    }
    
    // Generamos actividades para cada bloque del día
    const actividades = {
        manana: generarActividadesAleatorias(aleatorio1a5(), 4, 12),   // 4:00 - 12:00
        tarde: generarActividadesAleatorias(aleatorio1a5(), 12, 20),   // 12:00 - 20:00
        noche: generarActividadesAleatorias(aleatorio1a5(), 20, 4)     // 20:00 - 4:00 (del día siguiente)
    };
    
    // Función que crea actividades aleatorias dentro de un rango horario
    function generarActividadesAleatorias(cantidad, horaInicio, horaFin) {
        const result = [];
        for (let i = 0; i < cantidad; i++) {
            const actividad = actividadesPosibles[Math.floor(Math.random() * actividadesPosibles.length)];
            result.push({
                nombre: actividad.nombre,
                hora: generarHoraAleatoria(horaInicio, horaFin),
                musica: actividad.musica
            });
        }

        // Ordenamos por hora considerando si cruza la medianoche
        return result.sort((a, b) => {
            const horaA = parseInt(a.hora.split(':')[0]);
            const horaB = parseInt(b.hora.split(':')[0]);

            if (horaInicio > horaFin) {
                if (horaA >= 20) return horaB >= 20 ? horaA - horaB : -1;
                if (horaB >= 20) return 1;
                return horaA - horaB;
            }
            return horaA - horaB;
        });
    }
    
    // Generamos una hora aleatoria entre los límites dados
    function generarHoraAleatoria(horaInicio, horaFin) {
        let hora;
        if (horaInicio < horaFin) {
            hora = horaInicio + Math.floor(Math.random() * (horaFin - horaInicio));
        } else {
            hora = (horaInicio + Math.floor(Math.random() * (24 - horaInicio + horaFin))) % 24;
        }
        const minuto = Math.random() > 0.5 ? "00" : "30";
        return `${hora}:${minuto}`;
    }
    
    // Mostramos actividades en la interfaz
    renderizarActividades('manana', actividades.manana);
    renderizarActividades('tarde', actividades.tarde);
    renderizarActividades('noche', actividades.noche);
    
    // Insertamos las actividades al DOM
    function renderizarActividades(seccion, listaActividades) {
        const contenedor = document.querySelector(`.${seccion} .actividades`);
        listaActividades.forEach(act => {
            const div = document.createElement('div');
            div.className = 'actividad';
            div.dataset.musica = act.musica || '';
            div.innerHTML = `
                <div class="nombre">${act.nombre}</div>
                <div class="hora">${act.hora}</div>
            `;
            contenedor.appendChild(div);
        });
    }
    
    // Verificamos si es hora de una actividad que tiene música
    function verificarHoraActividades() {
        const ahora = new Date();
        const horaActual = ahora.getHours();
        const minutoActual = ahora.getMinutes();
        const horaFormateada = `${horaActual}:${minutoActual < 10 ? '0' + minutoActual : minutoActual}`;
        
        // Detenemos cualquier audio previo
        audioMeditacion.pause();
        
        // Quitamos clase 'activa' de todas las actividades
        document.querySelectorAll('.actividad').forEach(act => {
            act.classList.remove('activa');
        });
        
        // Activamos actividad correspondiente a la hora
        document.querySelectorAll('.actividad').forEach(actividad => {
            const horaActividad = actividad.querySelector('.hora').textContent;
            if (horaActividad === horaFormateada) {
                actividad.classList.add('activa');
                const idAudio = actividad.dataset.musica;
                if (idAudio) {
                    const audio = document.getElementById(idAudio);
                    if (audio) {
                        audio.currentTime = 0;
                        audio.play();
                    }
                }
            }
        });
    }
    
    // Verificamos cada 20 segundos si hay alguna actividad activa
    setInterval(verificarHoraActividades, 20000);
    verificarHoraActividades(); // Comprobar inmediatamente al cargar la página
    
    // Manejo de galería de fotos
    
    const fotosButton = document.getElementById('fotos-button');
    const fotoGallery = document.getElementById('foto-gallery');
    const closeGallery = document.getElementById('close-gallery');
    const galleryContent = document.getElementById('gallery-content');
    
    // Solicitamos al servidor si hay fotos para este día
    function verificarFotos() {
        socket.emit('verificarFotos', { dia, mes });
    }
    
    // Cargamos y muestra fotos en la galería
    function cargarFotos(fotos) {
        galleryContent.innerHTML = ''; // Limpiar galería

        if (fotos && fotos.length > 0) {
            fotos.forEach(foto => {
                const img = document.createElement('img');
                img.src = foto;
                img.alt = `Foto del día ${dia} de ${nombreMes}`;
                galleryContent.appendChild(img);
            });
            fotoGallery.classList.add('open'); // Mostrar galería
        } else {
            galleryContent.innerHTML = '<p>No hay fotos disponibles para este día.</p>';
        }
    }
    
    // Evento: clic en botón de galería
    fotosButton.addEventListener('click', () => {
        verificarFotos();
    });

    // Evento: cerrar galería
    closeGallery.addEventListener('click', () => {
        fotoGallery.classList.remove('open');
    });

    // Recibir fotos desde el servidor
    socket.on('fotosDia', (data) => {
        cargarFotos(data.fotos);
    });
});
