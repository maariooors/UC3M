// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

// Variables globales
int a = 10, b = 20, c;

// Función para calcular el máximo de dos números
maximo(int x, int y) {  
    if (x > y) {
        return x;
    } else {
        return y;
    }
}

// Función para calcular el mínimo de dos números
minimo(int x, int y) {
    if (x < y) {
        return x;
    } else {
        return y;
    }
}

main() {
    // Uso de funciones
    c = maximo(2,5);
    printf("El máximo entre a y b es: %d\n", c);

    c = minimo(6,9);
    printf("El mínimo entre a y b es: %d\n", c);

    // Condicionales complejos
    if (a > 0 && b > 0) {
        printf("Ignora", "Ambos números son positivos\n");
    }  else {
        printf("Ignora", "Ambos números son cero\n");
    }
}
//@(main)

