// Lista con los nombres de los meses en español, para usar cuando queramos mostrar o referirnos a un mes
const meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

// Esta función genera un calendario en formato HTML para un mes dado
// dias = número de días del mes
// empezarDia = día de la semana en que empieza el mes (0=domingo, 1=lunes, etc.)
// meses = número del mes (1-12) para usar en los enlaces y etiquetas
function generarCalendario(dias, empezarDia, meses) {
    // Empezamos creando la tabla con la cabecera de los días de la semana
    let calendario = "<table class='calendario'><tr class='header'><th>Domingo</th><th>Lunes</th><th>Martes</th><th>Miércoles</th><th>Jueves</th><th>Viernes</th><th>Sábado</th></tr><tr>";
    
    // Rellenamos los días previos al inicio del mes con celdas vacías para mantener la estructura
    for (let i = 0; i < empezarDia; i++) {
        calendario += "<td></td>";
    }
    
    // Ahora recorremos cada día del mes para ponerlo en la tabla
    for (let day = 1; day <= dias; day++) {
        // Cuando llegamos al inicio de una nueva semana (domingo), cerramos la fila anterior y abrimos una nueva
        if ((empezarDia + day - 1) % 7 === 0 && day !== 1) {
            calendario += "</tr><tr>";
        }
        
        // Aquí creamos un enlace para cada día, que lleva a la vista 'horario.html' con parámetros para el día, mes y día de la semana
        // Así podemos mostrar horarios o actividades específicas para cada fecha
        calendario += `<td><a href="../views/horario.html?dia=${day}&mes=${meses}&diaSemana=${['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'][(empezarDia + day - 1) % 7]}">${day}</a></td>`;
    }
    
    // Cerramos la última fila y la tabla completa
    calendario += "</tr></table>";
    
    // Devolvemos el HTML generado para insertarlo donde queramos
    return calendario;
}

// Objeto con los calendarios pre-generados para cada mes del año 2025
// Los parámetros usados para cada mes son:
// - Número de días en el mes
// - Día de la semana que empieza el mes (0=domingo, 1=lunes, etc.)
// - Número del mes para los enlaces
// Estos valores están "hardcodeados" según el calendario de 2025, para no calcularlos dinámicamente
const calendarios = {
    1: generarCalendario(31, 3, 1), // Enero empieza en miércoles (3)
    2: generarCalendario(28, 6, 2), // Febrero empieza en sábado (6)
    3: generarCalendario(31, 6, 3), // Marzo empieza en sábado (6)
    4: generarCalendario(30, 2, 4), // Abril empieza en martes (2)
    5: generarCalendario(31, 4, 5), // Mayo empieza en jueves (4)
    6: generarCalendario(30, 0, 6), // Junio empieza en domingo (0)
    7: generarCalendario(31, 2, 7), // Julio empieza en martes (2)
    8: generarCalendario(31, 5, 8), // Agosto empieza en viernes (5)
    9: generarCalendario(30, 1, 9), // Septiembre empieza en lunes (1)
    10: generarCalendario(31, 3, 10), // Octubre empieza en miércoles (3)
    11: generarCalendario(30, 6, 11), // Noviembre empieza en sábado (6)
    12: generarCalendario(31, 1, 12)  // Diciembre empieza en lunes (1)
};

// Cuando la página esté cargada, insertamos el calendario de enero (mes 1) en el contenedor con id 'calendario-container'
// Esto hace que al cargar veamos el calendario por defecto para el primer mes
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("calendar-container").innerHTML = calendarios[1];
});
