#include <stdio.h>

int global_var = 10;
int global_array[3];

otra_funcion() {
    int i = 0;
    global_array[0] = 1;
    global_array[1] = 2;
    global_array[2] = 3;
    while (i < 3) {
        printf("Número: %d\n", global_array[i]);
        i = i+1;
    }
}

suma(int a, int b) {
    int resultado = 0;
    resultado = a + b;
    return resultado;
}

main() {
    int x = 5;
    int y = 3;
    int total = 0;
    int i;
    total = suma(x, y);

    if (total > 5) {
        puts("Suma mayor que cinco");
    } else {
        puts("Suma menor o igual a cinco");
    }

    for (i = 0; i < 3; i = i+1) {
        puts("Hola");
        i = i+1;
    }

    otra_funcion();

    return 0;
}
//@ (main)
