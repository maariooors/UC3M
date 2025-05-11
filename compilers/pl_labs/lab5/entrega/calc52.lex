%{
#include "calc52.tab.h"
#include <stdio.h>
%}

%%

[ \t]   ;

[A-Z]   {
            yylval.indice = yytext[0] - 'A';
            return VARIABLE;
         }

[a-z]   {
            yylval.indice = yytext[0] - 'a' + 26;
            return VARIABLE;
         }

[0-9]+(\.[0-9]+)?  {
                       yylval.valor = atof(yytext);
                       return NUMERO;
                   }

"+"     { return '+'; }
"-"     { return '-'; }
"/"     { return '/'; }
"="     { return '='; }
"("     { return '('; }
")"     { return ')'; }
\n      { return '\n'; }

.       { printf("Carácter no reconocido: %s\n", yytext); }

%%

int main(int argc, char **argv) {
    yyparse();
    return 0;
}

int yywrap() {
    return 1;
}