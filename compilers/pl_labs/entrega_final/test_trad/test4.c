// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

// Variables globales
int global_var = 10;
int global_array[5];
int resultado;

// Función para calcular el factorial de un número
factorial() {
    int n = global_var;  // Usamos la variable global
    int fact = 1;
    while (n > 0) {
        fact = fact * n;
        n = n - 1;
    }
    return fact;
}

// Función para calcular la suma de un array
suma_array() {
    int suma = 0, i;
    for (i = 0; i < 5; i = i + 1) {
        suma = suma + global_array[i];
    }
    return suma;
}

// Función para encontrar el máximo en un array
maximo_array() {
    int max = global_array[0], i;
    for (i = 1; i < 5; i = i + 1) {
        if (global_array[i] > max) {
            max = global_array[i];
        }
    }
    return max;
}

main() {
    int i, local_var = 5;

    // Inicialización del array global
    for (i = 0; i < 5; i = i + 1) {
        global_array[i] = i + 1;  // Valores: 1, 2, 3, 4, 5
    }

    // Uso de la función factorial
    resultado = factorial();
    printf("El factorial de global_var es: %d\n", resultado);

    // Uso de la función suma_array
    resultado = suma_array();
    printf("La suma de los elementos del array global es: %d\n", resultado);

    // Uso de la función maximo_array
    resultado = maximo_array();
    printf("El máximo valor en el array global es: %d\n", resultado);

    // Operaciones con arrays y condicionales
    for (i = 0; i < 5; i = i + 1) {
        if (global_array[i] % 2 == 0) {
            printf("global_array[%d] = %d es par\n", i, global_array[i]);
        } else {
            printf("global_array[%d] = %d es impar\n", i, global_array[i]);
        }
    }

    // Bucle anidado para imprimir una matriz
    printf("Ignora", "Matriz 3x3:\n");
    for (i = 0; i < 3; i = i + 1) {
        int j;
        for (j = 0; j < 3; j = j + 1) {
            printf("%d ", i * j);
        }
        printf("Ignora", "\n");
    }

    // Condicionales complejos
    if (global_var > 0 && local_var > 0) {
        printf("Ignora", "Ambas variables son positivas\n");
    }  else {
        printf("Ignora", "Ambas variables son cero\n");
    }

    // Modificación de un elemento del array
    global_array[2] = 42;
    printf("Nuevo valor de global_array[2]: %d\n", global_array[2]);

    // Impresión final
    puts("Prueba avanzada completada.");
}
//@(main)




