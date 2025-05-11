// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

// Variables globales
int vector[5];  // Declaración sin inicialización
int resultado;

main() {
    int i;

    // Inicialización del array global
    vector[0] = 1;
    vector[1] = 2;
    vector[2] = 3;
    vector[3] = 4;
    vector[4] = 5;

    // Multiplicación de los elementos del vector
    for (i = 0; i < 5; i = i + 1) {
        vector[i] = vector[i] * 2;
        printf("vector[%d] = %d\n", i, vector[i]);
    }

    // Suma de los elementos del vector
    resultado = 0;
    for (i = 0; i < 5; i = i + 1) {
        resultado = resultado + vector[i];
    }
    printf("La suma de los elementos del vector es: %d\n", resultado);

    // Modificación de un elemento del vector
    vector[2] = 42;
    printf("Nuevo valor de vector[2]: %d\n", vector[2]);
}
//@(main)

