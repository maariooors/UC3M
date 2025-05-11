%{ /* Seccion 1 Declaraciones de C y bison */
#include <stdio.h>
#define YYSTYPE double
%}
/* Seccion 2 Declaraciones de bison */
%%
/* Seccion 3 Sint - Semantico */
axioma: expresion '\n' { printf ("Expresion=%lf\n", $1); }
;
expresion:    operando { $$ = $1; }
            | operando '+' expresion { $$ = $1 + $3; }
            | operando '-' expresion { $$ = $1 - $3; }
            | operando '*' expresion { $$ = $1 * $3; }
            | operando '/' expresion { $$ = $1 / $3; }
            ;
operando:     numero { $$ = $1; }
            ;
numero:       '0' { $$ = 0 ; }
            | '1' { $$ = 1 ; }
            | '2' { $$ = 2 ; }
            | '3' { $$ = 3 ; }
            | '4' { $$ = 4 ; }
            | '5' { $$ = 5 ; }
            | '6' { $$ = 6 ; }
            | '7' { $$ = 7 ; }
            | '8' { $$ = 8 ; }
            | '9' { $$ = 9 ; }
            ;
%%
/* Seccion 4 Codigo en C */
int yyerror (char *mensaje) {
    fprintf (stderr, "%s\n", mensaje) ;
}
int yylex (){
    unsigned char c ;
    do {
        c = getchar () ;
    } while (c == ' ') ;
    return c ;
}

int main (){
    while (1) {
        yyparse () ;
    }

}