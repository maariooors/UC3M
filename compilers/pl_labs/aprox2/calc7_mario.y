%{                      // SECCION 1
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern int yylex () ;
extern int yyerror () ;

char temp [2048] ;

# define FF fflush(stdout);

char *mi_malloc (int nbytes)
{
    char *p ;
    static long int nb = 0;
    static int nv = 0 ;

    p = malloc (nbytes) ;
    if (p == NULL) {
        fprintf (stderr, "No queda memoria para %d bytes mas\n", nbytes) ;
        fprintf (stderr, "Reservados %ld bytes en %d llamadas\n", nb, nv) ;
        exit (0) ;
    }
    nb += (long) nbytes ;
    nv++ ;

    return p ;
}

char *genera_cadena (char *nombre)
{
    char *p ;
    int l ;

    l = strlen (nombre)+1 ;
    p = (char *) mi_malloc (l) ;
    strcpy (p, nombre) ;

    return p ;
}

char *int_to_string(int n)
{
    sprintf(temp, "%d", n);
    return genera_cadena(temp);
}

char *char_to_string(char c)
{
    sprintf(temp, "%c", c);
    return genera_cadena(temp);
}


typedef struct {
    int valor ;
    int indice ;
    char *cadena ;
} t_attr ;

# define YYSTYPE t_attr // Esto dice que todos los tokens del parser van a ser de la estructura t_attr



%}

// SECCION 2

%token  NUMERO
%token  VARIABLE

%right  '='             //  es la ultima operacion que se debe realizar
%left   '+' '-'         //  menor orden de precedencia
%left   '*' '/'         //  orden de precedencia intermedio
%left   SIGNO_UNARIO    //  mayor orden de precedencia
%%
                        // SECCION 3: Gramatica - Semantico


axioma:         expresion '\n'				{ printf ("%s \n", $1.cadena ) ; }
                r_expr					    { ; }
            |   VARIABLE '=' expresion '\n'	{ printf ("= %c %s \n", $1.indice, $3.cadena ) ;  }
                r_expr					    { ; }
            ;


r_expr:     /* lambda */			    { ; }

            |   axioma					{ sprintf (temp, "%s", $1.cadena ) ;
                                        $$.cadena = genera_cadena (temp); }
            ;

expresion:      termino					        { sprintf (temp, "%s", $1.cadena ) ;
                                                $$.cadena = genera_cadena (temp); }

            |   expresion '+' expresion   		{ sprintf (temp, "( + %s %s )", $1.cadena, $3.cadena ) ;
                                                $$.cadena = genera_cadena (temp); }

            |   expresion '-' expresion   		{ sprintf (temp, "( - %s %s )", $1.cadena, $3.cadena ) ;
                                                $$.cadena = genera_cadena (temp); }

            |   expresion '*' expresion   		{ sprintf (temp, "( * %s %s )", $1.cadena, $3.cadena ) ;
                                                $$.cadena = genera_cadena (temp); }

            |   expresion '/' expresion   		{ sprintf (temp, "( / %s %s )", $1.cadena, $3.cadena ) ;
                                                $$.cadena = genera_cadena (temp); }
            ;

termino:        operando				            { sprintf (temp, "%s", $1.cadena ) ;
                                                    $$.cadena = genera_cadena (temp); }

            |   '+' operando %prec SIGNO_UNARIO		{ sprintf (temp, "+ %s", $2.cadena ) ;
                                                    $$.cadena = genera_cadena (temp); }

            |   '-' operando %prec SIGNO_UNARIO		{ sprintf (temp, "+ %s", $2.cadena ) ;
                                                     $$.cadena = genera_cadena (temp); }


            ;

operando:       VARIABLE				{ sprintf (temp, "%c", $1.indice ) ;
                                        $$.cadena = genera_cadena (temp); }

            |   NUMERO					{ $$.cadena = int_to_string($1.valor) ; }

            |   '(' expresion ')'		{ sprintf (temp, "%s", $2.cadena ) ;
                                        $$.cadena = genera_cadena (temp); }
            ;

%%

                        /* SECCION 4  Codigo en C */
int n_linea = 1 ;

int yyerror (mensaje)
char *mensaje ;
{
    fprintf (stderr, "%s en la linea %d\n", mensaje, n_linea) ;
}



int yylex ()
{
    unsigned char c ;

    do {
         c = getchar () ;
    } while (c == ' ' || c == '\r') ;

    if (c == '.' || (c >= '0' && c <= '9')) {
         ungetc (c, stdin) ;
         scanf ("%d", &yylval.valor) ;
         return NUMERO ;
    }

    if ((c >= 'A' && c <= 'Z') ||
    		 (c >= 'a' && c <= 'z')) {
         yylval.indice = c;
         return VARIABLE ;
    }

    if (c == '\n')
          n_linea++ ;
    return c ;
}


int main ()
{
    yyparse () ;
}
