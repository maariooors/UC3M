// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

// Variables globales
int global_array[5];
int resultado;

main() {
    int i, j;
    int local_array[3]; 

    // Inicialización del array local
    local_array[0] = 10;
    local_array[1] = 20;
    local_array[2] = 30;

    // Inicialización del array global
    global_array[0] = 1;
    global_array[1] = 2;
    global_array[2] = 3;
    global_array[3] = 4;
    global_array[4] = 5;

    // Suma de elementos del array global
    resultado = 0;
    for (i = 0; i < 5; i = i + 1) {
        resultado = resultado + global_array[i];
    }
    printf("La suma de los elementos del array global es: %d\n", resultado);

    // Producto de elementos del array local
    resultado = 1;
    for (i = 0; i < 3; i = i + 1) {
        resultado = resultado * local_array[i];
    }
    printf("El producto de los elementos del array local es: %d\n", resultado);

    // Bucles anidados
    for (i = 0; i < 3; i = i + 1) {
        for (j = 0; j < 2; j = j + 1) {
            printf("Iteración: i = %d, j = %d\n", i, j);
        }
    }
}
//@(main)

