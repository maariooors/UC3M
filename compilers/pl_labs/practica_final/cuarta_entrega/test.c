// frontend ./trad <test.c > test.l ; clisp < test.l
// backend  ./trad < test.c > test.l ; ./back < test.l > test.f ; gforth < test.f

//----------------------------------------------------------------------------------


#include <stdio.h>

suma(int a, int b) {
    return a + b;
}

producto(int a, int b) {
    return a * b;
}

main() {
    int x = 5, y = 10;
    printf("La suma de x e y es: %d\n", suma(x, y));
    printf("El producto de x e y es: %d\n", producto(x, y));
}
//@(main)
