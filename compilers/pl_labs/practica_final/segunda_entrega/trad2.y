// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

%{                          // SECCION 1 Declaraciones de C-Yacc

#include <stdio.h>
#include <ctype.h>            // declaraciones para tolower
#include <string.h>           // declaraciones para cadenas
#include <stdlib.h>           // declaraciones para exit ()

#define FF fflush(stdout);    // para forzar la impresion inmediata

int yylex () ;
int yyerror () ;
char *mi_malloc (int) ;
char *gen_code (char *) ;
char *int_to_string (int) ;
char *char_to_string (char) ;

char temp [2048] ;

// Abstract Syntax Tree (AST) Node Structure

typedef struct ASTnode t_node ;

struct ASTnode {
    char *op ;
    int type ;		// leaf, unary or binary nodes
    t_node *left ;
    t_node *right ;
} ;


// Definitions for explicit attributes

typedef struct s_attr {
    int value ;    // - Numeric value of a NUMBER
    char *code ;   // - to pass IDENTIFIER names, and other translations
    t_node *node ; // - for possible future use of AST
} t_attr ;

#define YYSTYPE t_attr

%}

// Definitions for explicit attributes

%token NUMBER
%token IDENTIF       // Identificador=variable
%token INTEGER       // identifica el tipo entero
%token STRING
%token MAIN          // identifica el comienzo del proc. main
%token WHILE         // identifica el bucle main
%token PUTS
%token PRINTF


%right '='                     // es la ultima operacion que se debe realizar
%left OR AND
%left DIST EQUAL
%left '<' '>' GREATEREQ LESSEQ
%left MOD
%right NOT
%left '+' '-'                  // menor orden de precedencia
%left '*' '/'                  // orden de precedencia intermedio
%left UNARY_SIGN               // mayor orden de precedencia

// Seccion 3 Gramatica - Semantico

%%

// ---------------------------SUPERAXIOMA--------------------------------------------

superAxioma: listaDeclaracionVar declaracionFun {

                if ($1.code == NULL) {
                    printf ("%s\n", $2.code);  // Solo declaracionFun si listaDeclaracionVar es vacía
                } else {
                    printf ("%s %s\n", $1.code, $2.code);  // Ambos si hay declaraciones
                }
             }

             r_superAxioma { ; }

             ;

r_superAxioma:                       { $$.code = NULL; } // Lambda
            | superAxioma            { $$ = $1; }
            ;

// ----------------------------------------------------------------------------------

// ---------------------------DECLARACION FUNCIONES----------------------------------

declaracionFun: MAIN '(' ')' '{' axioma '}' { sprintf (temp, "(defun main () %s )", $5.code) ;
                                              $$.code = gen_code (temp) ; }

                ;

// ----------------------------------------------------------------------------------

// ----------------------------------AXIOMA------------------------------------------

axioma:     sentencia r_axioma     {
                if ($2.code == NULL) {
                   sprintf (temp, "%s", $1.code) ;
               } else {
                   sprintf (temp, "%s %s", $1.code, $2.code) ;
               }
               $$.code = gen_code (temp) ;
            }
            ;

r_axioma:                       { $$.code = NULL; } // Lambda
            | axioma            { $$ = $1; }
            ;

// ----------------------------------------------------------------------------------

// ----------------------------------SENTENCIA---------------------------------------

sentencia:  PRINTF '(' STRING elem')' ';' { sprintf (temp, "%s", $4.code) ;
                                            $$.code = gen_code (temp) ; }

            | PUTS '(' STRING ')' ';'     { sprintf (temp, "(print \"%s\")", $3.code) ;
                                            $$.code = gen_code (temp) ; }

            | IDENTIF '=' expresion ';'   { sprintf (temp, "(setq %s %s)", $1.code, $3.code) ;
                                            $$.code = gen_code (temp) ; }

            | creacion ';'                { $$ = $1 ; }

            | bucle                       { $$ = $1 ; }

            ;

// ----------------------------------------------------------------------------------

// ----------------------------------BUCLES------------------------------------------

bucle: WHILE '(' expresion ')' '{' axioma '}' { sprintf (temp, "(loop while %s do %s)", $3.code, $6.code) ;
                                                $$.code = gen_code (temp) ; }


// ----------------------------------------------------------------------------------

// ----------------------------------ELEM--------------------------------------------

elem:    ','  expresion r_elem  {
             if ($3.code == NULL) {
                sprintf (temp, "(princ %s)", $2.code);
            } else {
                sprintf (temp, "(princ %s) %s", $2.code, $3.code);
            }
            $$.code = gen_code(temp);
        }
        ;

        | ','  STRING r_elem  {
               if ($3.code == NULL) {
                  sprintf (temp, "(princ \"%s\")", $2.code);
              } else {
                  sprintf (temp, "(princ \"%s\") %s", $2.code, $3.code);
              }
              $$.code = gen_code(temp);
          }
          ;

r_elem:                       { $$.code = NULL; } // Lambda
            | elem            { $$ = $1; }
            ;

// ----------------------------------------------------------------------------------

// -------------------------------DECLARACION VARIABLES-------------------------------

listaDeclaracionVar:               { $$.code = NULL; } // Lambda

                    | creacion ';' { $$ = $1 ; }

                    ;

creacion:    INTEGER IDENTIF asignacion {
                if ($3.code == NULL) {
                    sprintf (temp, "(setq %s 0)", $2.code);  // Valor por defecto 0 si no hay asignación
                } else {
                    sprintf (temp, "(setq %s %s)", $2.code, $3.code);
                }
                $$.code = gen_code(temp);
            }
            ;

asignacion:   { $$.code = NULL; } // Lambda

            | '=' NUMBER concatenacion   {
                if ($3.code == NULL) {
                    sprintf (temp, "%d", $2.value);
                } else {
                    sprintf (temp, "%d) %s", $2.value, $3.code);
                }
                $$.code = gen_code(temp);

            }
            ;


concatenacion: { $$.code = NULL; } // Lambda
             | ',' IDENTIF asignacion {
                 if ($3.code == NULL) {
                     sprintf(temp, "(setq %s 0)", $2.code);
                 } else {
                     sprintf(temp, "(setq %s %s", $2.code, $3.code);
                 }
                 $$.code = gen_code(temp);
               }
             ;

// ----------------------------------------------------------------------------------

// ----------------------------------EXPRESION---------------------------------------

expresion:    termino                           { $$ = $1 ; }

            | expresion '+' expresion           { sprintf (temp, "(+ %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion '-' expresion           { sprintf (temp, "(- %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion '*' expresion           { sprintf (temp, "(* %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion '/' expresion           { sprintf (temp, "(/ %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion OR expresion            { sprintf (temp, "(or %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion AND expresion           { sprintf (temp, "(and %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion GREATEREQ expresion     { sprintf (temp, "(>= %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion LESSEQ expresion        { sprintf (temp, "(<= %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion EQUAL expresion         { sprintf (temp, "(== %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion DIST expresion          { sprintf (temp, "(!= %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion MOD expresion           { sprintf (temp, "(%% %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            // | expresion NOT expresion           { sprintf (temp, "(! %s %s)", $3.code, $1.code) ;
            //                                       $$.code = gen_code (temp) ; }
            | expresion '<' expresion           { sprintf (temp, "(< %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            | expresion '>' expresion           { sprintf (temp, "(> %s %s)", $1.code, $3.code) ;
                                                  $$.code = gen_code (temp) ; }
            ;

// ----------------------------------------------------------------------------------

// ---------------------------------TERMINO------------------------------------------

termino:        operando                           { $$ = $1 ; }
            |   '+' operando %prec UNARY_SIGN      { $$ = $1 ; }
            |   '-' operando %prec UNARY_SIGN      { sprintf (temp, "(- %s)", $2.code) ;
                                                     $$.code = gen_code (temp) ; }
            ;

// ----------------------------------------------------------------------------------

// ---------------------------------OPERANDO-----------------------------------------

operando:       IDENTIF                  { sprintf (temp, "%s", $1.code) ;
                                           $$.code = gen_code (temp) ; }
            |   NUMBER                   { sprintf (temp, "%d", $1.value) ;
                                           $$.code = gen_code (temp) ; }
            |   '(' expresion ')'        { $$ = $2 ; }
            ;

// ----------------------------------------------------------------------------------

// SECCION 4    Codigo en C

%%

int n_line = 1 ;

int yyerror (mensaje)
char *mensaje ;
{
    fprintf (stderr, "%s en la linea %d\n", mensaje, n_line) ;
    printf ( "\n") ;	// bye
}

char *int_to_string (int n)
{
    sprintf (temp, "%d", n) ;
    return gen_code (temp) ;
}

char *char_to_string (char c)
{
    sprintf (temp, "%c", c) ;
    return gen_code (temp) ;
}

char *my_malloc (int nbytes)       // reserva n bytes de memoria dinamica
{
    char *p ;
    static long int nb = 0;        // sirven para contabilizar la memoria
    static int nv = 0 ;            // solicitada en total

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


/***************************************************************************/
/********************** Seccion de Palabras Reservadas *********************/
/***************************************************************************/

typedef struct s_keyword { // para las palabras reservadas de C
    char *name ;
    int token ;
} t_keyword ;

t_keyword keywords [] = { // define las palabras reservadas y los
    "main",        MAIN,           // y los token asociados
    "int",         INTEGER,
    "puts",        PUTS,
    "printf",      PRINTF,
    "while",       WHILE,
    "||",          OR,
    "&&",          AND,
    "<=",          LESSEQ,
    ">=",          GREATEREQ,
    "!=",          DIST,
    "==",          EQUAL,
    "%",           MOD,
    "!",           NOT,
    NULL,          0               // para marcar el fin de la tabla
} ;

t_keyword *search_keyword (char *symbol_name)
{                                  // Busca n_s en la tabla de pal. res.
                                   // y devuelve puntero a registro (simbolo)
    int i ;
    t_keyword *sim ;

    i = 0 ;
    sim = keywords ;
    while (sim [i].name != NULL) {
	    if (strcmp (sim [i].name, symbol_name) == 0) {
		                             // strcmp(a, b) devuelve == 0 si a==b
            return &(sim [i]) ;
        }
        i++ ;
    }

    return NULL ;
}


/***************************************************************************/
/******************* Seccion del Analizador Lexicografico ******************/
/***************************************************************************/

char *gen_code (char *name)     // copia el argumento a un
{                                      // string en memoria dinamica
    char *p ;
    int l ;

    l = strlen (name)+1 ;
    p = (char *) my_malloc (l) ;
    strcpy (p, name) ;

    return p ;
}


int yylex ()
{
// NO MODIFICAR ESTA FUNCION SIN PERMISO
    int i ;
    unsigned char c ;
    unsigned char cc ;
    char ops_expandibles [] = "!<=|>%&/+-*" ;
    char temp_str [256] ;
    t_keyword *symbol ;

    do {
        c = getchar () ;

        if (c == '#') {	// Ignora las lineas que empiezan por #  (#define, #include)
            do {		//	OJO que puede funcionar mal si una linea contiene #
                c = getchar () ;
            } while (c != '\n') ;
        }

        if (c == '/') {	// Si la linea contiene un / puede ser inicio de comentario
            cc = getchar () ;
            if (cc != '/') {   // Si el siguiente char es /  es un comentario, pero...
                ungetc (cc, stdin) ;
            } else {
                c = getchar () ;	// ...
                if (c == '@') {	// Si es la secuencia //@  ==> transcribimos la linea
                    do {		// Se trata de codigo inline (Codigo embebido en C)
                        c = getchar () ;
                        putchar (c) ;
                    } while (c != '\n') ;
                } else {		// ==> comentario, ignorar la linea
                    while (c != '\n') {
                        c = getchar () ;
                    }
                }
            }
        } else if (c == '\\') c = getchar () ;

        if (c == '\n')
            n_line++ ;

    } while (c == ' ' || c == '\n' || c == 10 || c == 13 || c == '\t') ;

    if (c == '\"') {
        i = 0 ;
        do {
            c = getchar () ;
            temp_str [i++] = c ;
        } while (c != '\"' && i < 255) ;
        if (i == 256) {
            printf ("AVISO: string con mas de 255 caracteres en linea %d\n", n_line) ;
        }		 	// habria que leer hasta el siguiente " , pero, y si falta?
        temp_str [--i] = '\0' ;
        yylval.code = gen_code (temp_str) ;
        return (STRING) ;
    }

    if (c == '.' || (c >= '0' && c <= '9')) {
        ungetc (c, stdin) ;
        scanf ("%d", &yylval.value) ;
//         printf ("\nDEV: NUMBER %d\n", yylval.value) ;        // PARA DEPURAR
        return NUMBER ;
    }

    if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')) {
        i = 0 ;
        while (((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') ||
            (c >= '0' && c <= '9') || c == '_') && i < 255) {
            temp_str [i++] = tolower (c) ;
            c = getchar () ;
        }
        temp_str [i] = '\0' ;
        ungetc (c, stdin) ;

        yylval.code = gen_code (temp_str) ;
        symbol = search_keyword (yylval.code) ;
        if (symbol == NULL) {    // no es palabra reservada -> identificador antes vrariabre
//               printf ("\nDEV: IDENTIF %s\n", yylval.code) ;    // PARA DEPURAR
            return (IDENTIF) ;
        } else {
//               printf ("\nDEV: OTRO %s\n", yylval.code) ;       // PARA DEPURAR
            return (symbol->token) ;
        }
    }

    if (strchr (ops_expandibles, c) != NULL) { // busca c en ops_expandibles
        cc = getchar () ;
        sprintf (temp_str, "%c%c", (char) c, (char) cc) ;
        symbol = search_keyword (temp_str) ;
        if (symbol == NULL) {
            ungetc (cc, stdin) ;
            yylval.code = NULL ;
            return (c) ;
        } else {
            yylval.code = gen_code (temp_str) ; // aunque no se use
            return (symbol->token) ;
        }
    }

//    printf ("\nDEV: LITERAL %d #%c#\n", (int) c, c) ;      // PARA DEPURAR
    if (c == EOF || c == 255 || c == 26) {
//         printf ("tEOF ") ;                                // PARA DEPURAR
        return (0) ;
    }

    return c ;
}


int main ()
{
    yyparse () ;
}
