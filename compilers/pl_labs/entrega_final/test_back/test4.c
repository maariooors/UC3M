// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

int a = 0;
int b;

main() {
    if (a == 0) {
        b = 123;
        printf("b: %d\n", b);
    } else {
        b = 456;
        printf("b: %d\n", b);
    }

    if (a == 0) {
        printf("Ignora", "a es igual a 0\n");
    } else {
        printf("Ignora", "a no es igual a 0\n");
    }
}
//@(main)

