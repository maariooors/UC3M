// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <stdio.h>

int contador = 0;
int acumulador = 0;
int auxiliar;

main() {
    while (contador < 8) {
        printf("Iteración número: %d\n", contador);
        acumulador = contador;

        while (acumulador > 0) {
            auxiliar = acumulador;
            if (auxiliar % 2 == 1) {
                puts("Número impar detectado");
            } else {
                puts("Número par detectado");
            }
            acumulador = acumulador - 1;
        }

        contador = contador + 1;
    }
}
//@(main)




