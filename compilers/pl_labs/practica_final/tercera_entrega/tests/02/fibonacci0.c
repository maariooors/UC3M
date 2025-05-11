#include <stdio.h>

// Tail recursive Fibonacci, es mas eficiente

fibonacci (int a, int b, int n) {
	int retorno;

	if (n < 2) {
		return b ;
	} else {
		return fibonacci (b, a+b , n-1) ;
	}
}

main ()
{
	int resultado;
	int i ;

    puts ("Sucesion de Fibonacci") ;

    for (i = 0 ; i < 47 ; i = i + 1) {
		resultado = fibonacci (0, 1, i) ;
		printf ("%d %s %d", i, " ", resultado) ;
		puts (" ") ;
    }
}

//@ (main)

