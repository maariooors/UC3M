// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

// Variables globales
int global_var = 10;
int another_global_var = 20;
int global_array[5];

// Función para sumar dos números
suma() {
    int a = 5, b = 10;
    return a + b;
}

// Función para multiplicar dos números
producto() {
    int a = 5, b = 10;
    return a * b;
}

main() {
    // Variables locales
    int local_var = 5, another_local_var = 15;
    int local_array[3];
    int i, j;

    // Inicialización del array global
    global_array[0] = 1;
    global_array[1] = 2;
    global_array[2] = 3;
    global_array[3] = 4;
    global_array[4] = 5;

    // Inicialización de un array local
    for (i = 0; i < 3; i = i + 1) {
        local_array[i] = i * 2;
        printf("local_array[%d] = %d\n", i, local_array[i]);
    }

    // Uso de variables globales
    printf("Suma de variables globales: %d\n", suma());
    printf("Producto de variables globales: %d\n", producto());

    // Bucle while
    i = 0;
    while (i < 3) {
        printf("Iteración del bucle while: %d\n", i);
        i = i + 1;
    }

    // Bucle for
    for (j = 0; j < 5; j = j + 1) {
        printf("global_array[%d] = %d\n", j, global_array[j]);
    }

    // Condicional if/else
    if (local_var < another_local_var) {
        puts("local_var es menor que another_local_var");
    } else {
        puts("local_var no es menor que another_local_var");
    }

    // Uso de return en funciones
    int resultado_suma = suma();
    int resultado_producto = producto();
    printf("Resultado de la suma: %d\n", resultado_suma);
    printf("Resultado del producto: %d\n", resultado_producto);

    // Uso de vectores
    global_array[2] = 42;
    printf("Nuevo valor de global_array[2]: %d\n", global_array[2]);

    // Impresión final
    puts("Prueba completa finalizada.");
}
//@(main)

