## BISON

Los archivos de bison están divididos en 4 secciones.
1. Sección de definiciones: Se declaran variables, librerias, funciones etc de C. Va entre los símbolos %{ y %}.
2. Sección de declaraciones: Se declaran los tipos de los tokens y los no terminales.
3. Sección de reglas: Se incorporan las reglas de la gramática. Va entre %% y %%.
4. Sección de código C: Se escribe el código C que se ejecutará en el parser.

Cuando tienes tokens, el tipo de los tokens se almacena en la variable yylval. Por defecto este valor es un entero.
No obstante, se puede cambiar mediante el uso de %union en la parte de declaraciones. Dentro de %union declaramos
el resto de tipos de token que nuestro parser va a procesar.

    %union {
        double n_double;
        int n_int;
    }

Una vez usado %union, si queremos acceder a los valores de los tokens, tendremos que escribir yylval.n_double
o yylval.n_int en este caso.

Para asignar estos valores a los tokens, lo haremos de la siguiente manera:

    %token <n_double> NUMERO
    %token <n_int> VARIABLE

En la zona del código C estamos obligados a crear una función yyerror() de la siguiente manera:

    int yyerror(char *mensaje) {
        fprintf(stderr, "%s\n", mensaje);
    }
    
Además, tendremos que crear una función main() que llame a yyparse().

    int main() {
        yyparse();
    }
    
En el caso de que no haya un analizador de léxico, en la zona final del código C se tiene que crear una función yylex()
que se encargue de leer los tokens de entrada.

Para devolver estos tokens de entrada se almacena el valor dentro de la variable yylval.TIPO_DE_VALOR y se
hace un return con el nombre del token.

     yylval.indice = LO_QUE_SEA;
     return VARIABLE;

En el caso de que si haya un analizador de léxico, se eliminará el yylex().

---
## FLEX

Los archivos de flex están divididos en 3 secciones.
1. Sección de definiciones: Se declaran variables, librerias, funciones etc de C. Va entre los símbolos %{ y %}.
2. Sección de reglas: Se incorporan las reglas de la gramática. Va entre %% y %%.
3. Sección de código C: Se escribe el código C que se ejecutará en el parser.

### SECCIÓN DE DEFINICIONES

En la zona de las definiciones tenemos siempre que incluir la salida del archivo bison que previamente habremos
compilado. Para ello usamos #include "nombre_del_archivo.tab.h". Además al haber eliminado las funciones main() y
yylex() del archIvo bison, tendremos que incluir "#include <stdio.h>" ya que crearemos el main() en este archivo.

### SECCIÓN DE REGLAS


En la zona de las reglas escribiremos las reglas de la gramática. Aquí hay que tener en cuenta muchas cosas.
1. Las reglas van entre "[]" y se acompañan al igual que en bison de {} para ver que hay que hacer cuando esa
regla se cumple.

2. [A-Z] significa que se acepta cualquier letra mayúscula.

3. [0-9] significa que se acepta cualquier número.

4. [a-zA-Z] significa que se acepta cualquier letra. Esto demuestra que si queremos poner varias normas dentro
de la misma regla, simplemente se pone una y después la otra.

5. Para concatenar reglas se pueden usar varios símbolos:

    - "+" significa que se acepta una o más veces.
    - "*" significa que se acepta cero o más veces.
    - "?" significa que se acepta cero o una vez.

    Estos símbolos se colocan al final de la regla.

6. Si queremos referirnos a un carácter en concreto como una barra, un menos, un más, etc, se hace entre "".

7. Los símbolos que usen "\" como "\n" o "\t" se ponen tal cual.

8. El punto es ".\\"

9. Cuando se cumpla una regla y queramos devolverla a un token se hará de la siguiente manera:

   - Para devolver un caracter haremos uso de yytext[0].

           yylval.indice = yytext[0];
           return VARIABLE;
    
   - Para devolver un texto lo haremos con yytext.

           [a-zA-Z][a-zA-Z0-9_]*    { yylval.sval = strdup(yytext);
                                      return VARIABLE; }

   - Para devolver un número lo podemos hacer de varias maneras.

           [0-9]+(\.[0-9]+)?  { yylval.valor = atof(yytext);
                                return NUMERO; }
    
           [0-9]+(\.[0-9]+)?  { sscanf(yytext, "%lf", &yylval.dval);
                                return NUMERO;

   - Para devolver un carácter en específico a un token lo haremos directamente:

           "="                { return ASIGNACION; }

10. Si no queremos devolver el valor leído a un token porque en el archivo bison se trata de un caracter literal,
lo retornamos directamente.

        "+"                { return '+'; }

11. En el caso de que no se cumpla ninguna regla y queramos evitar un error, haremos uso del "." de la siguiente
manera:

        .                 { printf("Carácter no reconocido: %s\n", yytext[0]); }
        .                 { return yytext[0]; }

    Lo que hagamos con este caracter no esperado dependerá de nosotros.

### SECCIÓN DE CÓDIGO C

En la zona de código C, estamos obligados siempre a crear la función yywrap() que devolverá un 1    