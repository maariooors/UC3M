// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

// Variables globales
int global_var = 10;
int global_array[3];

// Función para sumar dos números
suma() {
    int a = global_var, b = 5;
    return a + b;
}

// Función para multiplicar dos números
producto() {
    int a = global_var, b = 5;
    return a * b;
}

main() {
    int local_var = 5, resultado;
    int i;

    // Inicialización del array global
    global_array[0] = 1;
    global_array[1] = 2;
    global_array[2] = 3;

    // Uso de funciones
    resultado = suma();
    printf("La suma de global_var y local_var es: %d\n", resultado);

    resultado = producto();
    printf("El producto de global_var y local_var es: %d\n", resultado);

    // Operaciones con arrays
    for (i = 0; i < 3; i = i + 1) {
        global_array[i] = global_array[i] + i;
        printf("global_array[%d] = %d\n", i, global_array[i]);
    }

    // Condicionales y bucles
    if (global_var > 0) {
        printf("Ignora", "global_var es positivo\n");
    } else {
        printf("Ignora", "global_var no es positivo\n");
    }

    i = 0;
    while (i < 3) {
        printf("Iteración del bucle while: i = %d\n", i);
        i = i + 1;
    }
}
//@(main)

