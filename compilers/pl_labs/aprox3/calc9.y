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

// Abstract Syntax Tree (AST) Node Structure

typedef struct ASTnode t_node ;
struct ASTnode {
    char *op ; // simplified node information in form as a string
    int type ; // leaf, unary or binary nodes (0/1/2)
    t_node *left ;
    t_node *right ;
} ;

// Function to create a new AST node

t_node * createASTNode (char *op, int type, t_node *left, t_node *right) {
    t_node *node ;
    node = (t_node*) malloc (sizeof (t_node)) ;
    node->op = strdup (op) ; // duplicates string in memory
    node->type = type ; // binary, unary or leaf node
    node->left = left ;
    node->right = right ;
    return node ;
}

// Function to free AST

void freeAST (t_node *node) {
    if (node != NULL) {
        freeAST (node->left) ;
        freeAST (node->right) ;
        free (node->op) ;
        free (node) ;
    }
}

// Function to print AST in prefix notation

void printAST2Prefix (t_node *node) {
    if (node == NULL) {
        return ;
    } else if (node->type == 0) {
        printf ("%s ", node->op) ; // Leaf node
    } else if (node->type == 1) {
        printf ("( %s ", node->op) ; // Unary node
        printAST2Prefix (node->left) ;
        printf (") ") ;
    } else {
        printf ("( %s ", node->op) ; // Binary node
        printAST2Prefix (node->left) ;
        printAST2Prefix (node->right) ;
        printf (") ") ;
    }
}

typedef struct s_attr {
    int valor ;
    int indice ;
    char *cadena ;
    t_node *node ; // for AST
} t_attr ;


#define YYSTYPE t_attr

%}

// SECTION 2

%token NUMERO
%token VARIABLE
%right '=' // operator with the least precedence
%left '+' '-' //
%left '*' '/' //
%left SIGNO_UNARIO // operator with the highest precedence

%%

// SECTION 3: Grammar - Semantic Section

axioma:         sentencia '\n'       { printAST2Prefix($1.node); printf("\n"); }
                r_expr               { ; }


                | '@' expresion	'\n' { printAST2Prefix($2.node); printf("\n"); }
                r_expr               { ; }
                ;

sentencia:          expresion			     { $$.node = $1.node; }

                |   VARIABLE '=' sentencia   { $$.node = createASTNode (char_to_string ('='), 2, $1.node, $3.node) ; }
                ;

r_expr:     /* lambda */			    { ; }
            |   axioma					{ $$.node = $1.node; }
            ;

expresion:      termino					        { $$.node = $1.node; }

            |   expresion '+' expresion   		{ $$.node = createASTNode (char_to_string ('+'), 2, $1.node, $3.node) ; }

            |   expresion '-' expresion   		{ $$.node = createASTNode (char_to_string ('-'), 2, $1.node, $3.node) ; }

            |   expresion '*' expresion   		{ $$.node = createASTNode (char_to_string ('*'), 2, $1.node, $3.node) ; }

            |   expresion '/' expresion   		{ $$.node = createASTNode (char_to_string ('/'), 2, $1.node, $3.node) ; }


            ;

termino:        operando				            { $$.node = $1.node; }

            |   '+' operando %prec SIGNO_UNARIO		{ $$.node = createASTNode (char_to_string ('+'), 1, $2.node, NULL) ; }

            |   '-' operando %prec SIGNO_UNARIO		{ $$.node = createASTNode (char_to_string ('-'), 1, $2.node, NULL) ;  }
            ;

operando:       VARIABLE				{ $$.node = createASTNode (char_to_string ($1.indice+'A'), 0, NULL, NULL) ; }

            |   NUMERO					{ $$.node = createASTNode (int_to_string ($1.valor), 0, NULL, NULL) ; }

            |   '(' sentencia ')'		{ $$.node = $2.node; }
            ;

%%

/* SECTION 4 C Code */

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
