

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

expression:   termino                  { $$ = $1; }
            | expression '+' termino   { $$ = $1 + $3; }
            | expression '-' termino   { $$ = $1 - $3; }
            ;

termino:     factor                    { $$ = $1; }
            | termino '*' factor       { $$ = $1 * $3; }
            | termino '/' factor       { $$ = $1 / $3; }
            ;

factor:      operando                  { $$ = $1; }
            | '(' expression ')'       { $$ = $2; }
            | '-' factor               { $$ = -$2; }
            ;

operando:    numero                    { $$ = $1; }
            ;

numero:       digito                   { $$ = $1; }
            | numero digito            { $$ = $1 * 10 + $2; }
            ;

digito:       '0'                      { $$ = 0; }
            | '1'                      { $$ = 1; }
            | '2'                      { $$ = 2; }
            | '3'                      { $$ = 3; }
            | '4'                      { $$ = 4; }
            | '5'                      { $$ = 5; }
            | '6'                      { $$ = 6; }
            | '7'                      { $$ = 7; }
            | '8'                      { $$ = 8; }
            | '9'                      { $$ = 9; }
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

/**
    TODO: Expresiones como 1 - 1 - 1 no funcionan correctamente. El resultado debería ser -1.
*/

