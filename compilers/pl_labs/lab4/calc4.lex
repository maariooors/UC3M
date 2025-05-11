%{
#include "calc4.tab.h"  /* Incluir el archivo de cabecera generado por Bison */
extern int n_linea;     /* Declarar la variable externa para el número de línea */
%}

%%

[ \t]                    { ; } /* Ignorar espacios y tabuladores */

[0-9]+(\.[0-9]+)?        { sscanf(yytext, "%lf", &yylval.dval);  /* Leer un número flotante y asignarlo a yylval.dval */
                         return NUMERO;                         /* Devolver el token NUMERO */
}

[a-zA-Z][a-zA-Z0-9_]*    { yylval.sval = strdup(yytext);  /* Almacenar el nombre de la variable en yylval.sval */
                         return VARIABLE;                /* Devolver el token VARIABLE */
}

\n                   { n_linea++; return '\n'; } /* Incrementar el número de línea y devolver '\n' */

"="                  { return ASIGNACION; }      /* Devolver el token ASIGNACION */
"+"                  { return '+'; }             /* Devolver el carácter '+' */
"-"                  { return '-'; }             /* Devolver el carácter '-' */
"*"                  { return '*'; }             /* Devolver el carácter '*' */
"/"                  { return '/'; }             /* Devolver el carácter '/' */
"("                  { return '('; }             /* Devolver el carácter '(' */
")"                  { return ')'; }             /* Devolver el carácter ')' */
.                    { return yytext[0]; }       /* Devolver cualquier otro carácter tal cual */

%%

int yywrap() {
    return 1;
}