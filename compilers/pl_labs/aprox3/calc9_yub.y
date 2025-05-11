// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

// SECCION 1

%{
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


typedef struct ASTNode {
    char *valor;
    int numHijos;
    struct ASTNode *izq;
    struct ASTNode *der;
} ASTNode;

ASTNode *createASTNode(char *valor, int numHijos, ASTNode *izq, ASTNode *der) {
    ASTNode *node = (ASTNode *) malloc(sizeof(ASTNode));
    node->valor = strdup(valor);
    node->numHijos = numHijos;
    node->izq = izq;
    node->der = der;
    return node;
}

void printAST(ASTNode *node) {
    if (!node) return;
    if (node->num_hijos == 0) {
        printf("%s", node->valor);
    } else {
        printf("(%s ", node->valor);
        printAST(node->izq);
        if (node->num_hijos == 2) {
            printf(" ");
            printAST(node->der);
        }
        printf(")");
    }
}

typedef struct {
    int valor ;
    int indice ;
    char *cadena ;
    ASTNode *node;
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


axioma:         sentencia '\n'       { printAST($1.node); printf("\n"); }
                r_expr               { ; }


                | '@' expresion	'\n' { printAST($2.node); printf("\n"); }
                r_expr               { ; }
                ;

sentencia:      expresion			{ $$.node = $1.node ; }

                |   VARIABLE '=' sentencia          { $$.node = createASTNode("=", 2, createASTNode(char_to_string($1.indice + 'A'), 0, NULL, NULL), $3.node); }
                ;

r_expr:     /* lambda */			    { ; }
            |   axioma					{ sprintf (temp, "%s", $1.cadena ) ;
                                        $$.cadena = genera_cadena (temp); }
            ;

expresion:      termino					        { $$.node = $1.node; }

            |   expresion '+' expresion   		{$$.node = createASTNode("+", 2, $1.node, $3.node); }

            |   expresion '-' expresion   		{ $$.node = createASTNode("-", 2, $1.node, $3.node); }

            |   expresion '*' expresion   		{ $$.node = createASTNode("*", 2, $1.node, $3.node); }

            |   expresion '/' expresion   		{ $$.node = createASTNode("/", 2, $1.node, $3.node); }


            ;

termino:        operando				            { $$.node = $1.node; }

            |   '+' operando %prec SIGNO_UNARIO		{ $$.node = createASTNode("+", 1, $2.node, NULL); }

            |   '-' operando %prec SIGNO_UNARIO		{ $$.node = createASTNode("-", 1, $2.node, NULL); }
            ;

operando:       VARIABLE				{ $$.node = createASTNode(char_to_string($1.indice + 'A'), 0, NULL, NULL); }

            |   NUMERO					{ $$.node = createASTNode(int_to_string($1.valor), 0, NULL, NULL); }

            |   '(' sentencia ')'		{ $$.node = $2.node; }
            ;

%%


// SECCION 4  Codigo en C


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