// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

int a = 0;
int b = 0;
int c = 0;
int suma = 0;
int producto = 1;

main() {
    // Declaraciones iniciales
    a = 10;
    b = 20;
    printf("Ignora","Valores iniciales: a, b ", a, b);

    // Operaciones aritméticas
    suma = a + b;
    producto = a * b;
    printf("Ignora", "Suma de a y b", suma);
    printf("Ignora","Producto de a y b", producto);

    // Condicionales
    if (a == 10) {
        printf("Ignora","a es igual a 10");
    } else {
        printf("Ignora","a no es igual a 10");
    }

    if (b > 15 && b < 25) {
        printf("Ignora","b está entre 15 y 25");
    } else {
        printf("Ignora","b no está entre 15 y 25");
    }

    // Bucles anidados
    while (a > 0) {
        printf("Ignora","Valor de a", a);
        a = a - 1;

        c = b;
        while (c > 0) {
            if (c % 2 == 0) {
                printf("Ignora",c, "es par");
            } else {
                printf("Ignora",c, "es impar");
            }
            c = c - 1;
        }
    }

    // Operaciones combinadas
    a = 3;
    b = 4;
    c = a + b * 2;
    printf("Resultado de c = a + b * 2", c);

    // Condicional con múltiples ramas
    if (c > 10) {
        printf("Ignora","c es mayor que 10");
    } else {
        printf("Ignora","c es menor que 10");
    }

    // Bucle con condición compleja
    a = 0;
    b = 5;
    while (a < 10) {
        printf("a:, b:", a, b);
        a = a + 1;
        if (b > 0) {
            b = b - 1;
        }
    }
}
//@(main)
