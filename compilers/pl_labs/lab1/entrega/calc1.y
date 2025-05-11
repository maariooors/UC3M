// Grupo 3, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

/**

    LABORATORIO 1: EXPLICACIÓN

    En el PDF se explica como se ha obtenido la gramática y el porqué de las decisiones tomadas y de los
    patrones de diseño.

    El programa funciona de la siguiente manera:

        - Estas obligado a llamar a la función yyparse() en el main para que se ejecute el programa.

        - Esta automaticamente llama a la función yylex() que lee de la entrada estandar, y la cual
          nosotros sobreescrivimos y programamos para que ignore los espacios en blanco.

        - Una vez que yyparse() recibe el valor de yylex(), se ejecutará la gramática que hemos definido
          en el fichero de la siguiente manera: Ej (4+7) -> 11

                - Pila inicial []
                - Desplaza el 4 a la pila -> [4]
                - Reduce 4 → numero → operando → expresion -> [expresion]
                - Desplaza '+' -> [expresion, '+']
                - Comprueba si puede hacer algo con la pila actual, no puede
                - Reduce 7 → numero → operando → expression -> [expresion, "+", expresion]
                - Comrpueba si puede hacer algo con la pila actual, puede
                - Reduce expresion + expresion → expression -> [expression]
                - Desplaza '\n' -> [expression, '\n']
                - Reduce la pila entera a axioma y lo ejecuta -> Resultado = 11

          Nota: Los simbolos no terminales que se introcuden en la pila son reudcidos hasta que no se pueda hacer
          nada más con ellos, y además, cada vez que se introduce un nuevo no terminal en la pila, se comprueba
          si se puede reducir la pila entera.

    NOTACIÓN:
    - SIMBOLO_NO_TERMINAL: Todas sus producciones que se separan por "|"
    - Para asignar a un NO_TERMINAL su producción, se pone al lado de esta las reglas.
      Esto se hace de la siguiente manera: {$$ = 0;}. El termino "$$" hace referencia el simbolo
      no terminal al que se le asigna la producción.

      En el caso de que no querramos asignar solo un terminal a un simbolo no terminal, se puede hacer
      de la siguiente manera: {$$ = $1 + $3;}, donde "$1" hace referencia al primer elemento de la producción
      y "$3" al tercero.

      Las concatenaciones se hacen con un simple espacio en blanco y los simbolos terminales se ponen
      entre comillas simples.
*/

%{

/* Sección 1: Declaraciones de C y bison */

# include <stdio.h>
# define YYSTYPE double
int yyerror (char *mensaje) ;
int yylex () ;

%}

/* Sección 2: Declaraciones de bison */

%%

/* Sección 3: Reglas sintácticas y acciones semánticas */

axioma:
    /* Vacío para permitir múltiples expresiones */
    | axioma expression '\n' { printf("Expresion = %.2lf\n", $2); }
    ;

expression:   operando                  { $$ = $1; }
            | operando '+' expression   { $$ = $1 + $3; }
            | operando '-' expression   { $$ = $1 - $3; }
            | operando '*' expression   { $$ = $1 * $3; }
            | operando '/' expression   { $$ = $1 / $3; }
            ;

operando:    numero                     { $$ = $1; }
            ;

numero:       '0'                       { $$ = 0; }
            | '1'                       { $$ = 1; }
            | '2'                       { $$ = 2; }
            | '3'                       { $$ = 3; }
            | '4'                       { $$ = 4; }
            | '5'                       { $$ = 5; }
            | '6'                       { $$ = 6; }
            | '7'                       { $$ = 7; }
            | '8'                       { $$ = 8; }
            | '9'                       { $$ = 9; }
            ;

%%

/* Sección 4: Código en C */

int yyerror (char *mensaje)
{
    fprintf (stderr, "%s\n", mensaje) ;
}

int yylex ()
{
    unsigned char c ;

    do {
         c = getchar () ;
    } while (c == ' ') ;

    return c ;
}

int main ()
{
  yyparse();
}