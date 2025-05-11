%{

# include <stdio.h>
# define YYSTYPE  double
double parte_decimal;

int yylex();
int yyerror(char *mensaje);


%}

/* Seccion 2  Declaraciones de bison   */

%token DIG


%%

/* Seccion 3  Sintactico - Semantico   */

axioma:      expresion '\n' { printf ("Expresion=%lf\n", $1) ; }  r_expr
           ;

r_expr:	   /* lambda */
           | axioma
           ;

expresion:   operando                { $$ = $1; }
           | '-' operando            { $$ = -$2; }
           | operando '+' expresion  { $$ = $1 + $3; }
           | operando '-' expresion  { $$ = $1 - $3; }
           | operando '*' expresion  { $$ = $1 * $3; }
           | operando '/' expresion  { $$ = $1 / $3; }
           ;

operando:    numero                  { $$ = $1; }
           | '('  expresion  ')'     { $$ = $2; }
           | '-' numero              { $$ = -$2; }
           ;

numero:      DIG          { $$ = $1; }
           | DIG numero   { $$ = $1 * 10 + $2; }
           | n_decimal    { $$ = $1; }
           ;

n_decimal: numero '.' numero {double parte_decimal = $3;
                                  while (parte_decimal >= 1.0) {
                                    parte_decimal /= 10;  // Mover el punto decimal a la izquierda
                                  }
                                  $$ = $1 + parte_decimal;  // Sumar la parte entera y la parte decimal
                                }
            | '.' numero {double parte_decimal = $2;
                            while (parte_decimal >= 1.0) {
                                parte_decimal /= 10;  // Mover el punto decimal a la izquierda
                            }
                            $$ = parte_decimal;  // Sumar la parte entera y la parte decimal
                           }
            ;


%%

/* Seccion 4  Codigo en C   */

int yyerror (char *mensaje) {
    fprintf (stderr, "%s\n", mensaje) ;
    return -1 ;
}


int yylex () {
    unsigned char c ;
    double valor ;

    do {
         c = getchar () ;
    } while (c == ' ') ;

    if (c >= '0' && c <= '9') {
         ungetc (c, stdin) ;
         scanf ("%lf", &valor) ;
         yylval = valor ;
         return DIG ;
    }

    return c ;
}


int main ()
{
    yyparse () ;
}
