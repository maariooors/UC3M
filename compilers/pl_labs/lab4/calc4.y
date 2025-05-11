%{

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int yylex(void);
void yyerror(char *mensaje);
double obtener_valor_variable(char *nombre);
double asignar_variable(char *nombre, double valor);

%}

%union { /* Sirve para decirle a la pila que se va a haber caracteres de diferentes tipos*/
    double dval;  /* Para números flotantes */
    char *sval;   /* Para cadenas (nombres de variables) */
}

%token <dval> NUMERO      /* Token para números flotantes */
%token <sval> VARIABLE    /* Token para nombres de variables */
%token ASIGNACION '='     /* Token para el operador de asignación */

%left '+' '-'             /* Menor orden de precedencia */
%left '*' '/'             /* Orden de precedencia intermedio */
%left SIGNO_UNARIO        /* Mayor precedencia para operadores unarios */
%right ASIGNACION         /* Asignación tiene menor precedencia y es asociativa a la derecha */

%type <dval> expresion asignacion  /* Declarar el tipo de retorno para expresiones y asignaciones */

%%

axioma:       expresion '\n' { printf("Expresion=%lf\n", $1); } r_expr
            | asignacion '\n' { printf("Asignacion realizada\n"); } r_expr
            ;

r_expr:     /* lambda */
            | axioma
            ;

asignacion:   VARIABLE ASIGNACION expresion { $$ = asignar_variable($1, $3); }
            ;

expresion:    NUMERO                   { $$ = $1; }
            | VARIABLE                 { $$ = obtener_valor_variable($1); }
            | expresion '+' expresion  { $$ = $1 + $3; }
            | expresion '-' expresion  { $$ = $1 - $3; }
            | expresion '*' expresion  { $$ = $1 * $3; }
            | expresion '/' expresion  { $$ = $1 / $3; }
            | '+' expresion %prec SIGNO_UNARIO          { $$ = $2; }
            | '-' expresion %prec SIGNO_UNARIO          { $$ = -$2; }
            | '(' expresion ')'                         { $$ = $2; }
            ;

%%

int n_linea = 1;
void yyerror (char *mensaje) {
    fprintf(stderr, "%s en la linea %d\n", mensaje, n_linea);
}

typedef struct {
    char nombre[50];  /* Nombre de la variable */
    double valor;     /* Valor de la variable */
} Variable;

Variable tabla_variables[100];  /* Tabla de variables */
int num_variables = 0;          /* Número de variables en la tabla */

/* Función para obtener el valor de una variable */
double obtener_valor_variable(char *nombre) {
    for (int i = 0; i < num_variables; i++) {
        if (strcmp(tabla_variables[i].nombre, nombre) == 0) {
            return tabla_variables[i].valor;  /* Retorna el valor si la variable existe */
        }
    }
    fprintf(stderr, "Advertencia: Variable '%s' no definida. Se asume 0.0.\n", nombre);
    return 0.0;  /* Retorna 0.0 si la variable no existe */
}

/* Función para asignar un valor a una variable */
double asignar_variable(char *nombre, double valor) {
    for (int i = 0; i < num_variables; i++) {
        if (strcmp(tabla_variables[i].nombre, nombre) == 0) {
            tabla_variables[i].valor = valor;  /* Actualiza el valor si la variable existe */
            return valor;
        }
    }
    if (num_variables < 100) {
        strcpy(tabla_variables[num_variables].nombre, nombre);
        tabla_variables[num_variables].valor = valor;
        num_variables++;
        return valor;
    }
    fprintf(stderr, "Error: Tabla de variables llena. No se puede agregar '%s'.\n", nombre);
    return 0.0;  /* Retorna 0.0 si la tabla está llena */
}

int main() {
    yyparse();
}