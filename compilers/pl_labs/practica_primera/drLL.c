// Grupo 403, Mario Ramos Salsón y Miguel Yubero Espinosa
// 100495849@alumnos.uc3m.es 100495984@alumnos.uc3m.es

#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define T_NUMBER 	1001        // To avoid ASCII conflicts
#define T_OPERATOR	1002        // To avoid ASCII conflicts
#define T_VARIABLE  1003        // To avoid ASCII conflicts

void ParseYourGrammar (void) ; 		/// Dummy Parser
void ParseAxiom (void) ;			/// Prototype for forward reference
void ParseExpression(void);

struct s_tokens {
	int token ;					// Here we store the current token/literal
	int old_token ; 			// Sometimes we need to check the previous token
	int number ;				// The value of the number
	int old_number ;			// old number value
	char variable_name [8] ;	/// variable name
	char old_var_name [8] ;		/// old variable name
	int token_val ;				// the arithmetic operator
	int old_token_val ;			// old arithmetic operator
} ;

struct s_tokens tokens = {0, 0, 0, -1, "", "", 0, -1}; // contains initial values


int line_counter = 1 ;


void update_old_token ()
{					/// Sometimes we need to check the previous token
	tokens.old_token = tokens.token ;
	tokens.old_number = tokens.number ;
	strcpy (tokens.old_var_name, tokens.variable_name) ;	/// Copy variable names
	tokens.old_token_val = tokens.token_val ;
}


void init_tokens ()
{ 								///  Not really neccesary
    tokens.token = 0;
	tokens.old_token = 0 ;
    tokens.number = 0 ;
    tokens.old_number = -1 ;
	strcpy (tokens.old_var_name, "") ;			/// erase old variable name
	strcpy (tokens.variable_name, "") ;			/// Erase variable name
    tokens.token_val = 0;
    tokens.old_token_val = -1;
}


int rd_lex ()
{
	int c ;
	int cc ;

	do {
		c = getchar () ;
		if (c == '\n')
			line_counter++ ;	// info for rd_syntax_error()
	} while (c == '\t' || c == ' ' || c == '\r') ;	/// \r is part of a newline in some Operating Systems

	if (isdigit (c)) {			/// Token Number is [Digit]+
		ungetc (c, stdin) ;		/// This returns one character to the standard input stream
		update_old_token () ;
		scanf ("%d", &tokens.number) ;
		tokens.token = T_NUMBER ;
		return (tokens.token) ;	// returns the Token for Variable
	}

	if (isalpha(c)) {  /// Token Variable of type Letter[Digit]?
        update_old_token () ;
		cc = getchar () ;
		if (isdigit (cc)) {
			sprintf (tokens.variable_name, "%c%c", c, cc) ;		/// This copies the LetterDigit name in the variable name
		} else {
			ungetc (cc, stdin) ;
			sprintf (tokens.variable_name, "%c", c) ;			/// This copies the single Letter name in the variable name
		}
		tokens.token = T_VARIABLE ;
        return (tokens.token) ;	// returns the Token for Variable
    }

	if (c == '+' || c == '-' || c == '*' || c == '/') {  /// Remember that = is returned as a literal
		update_old_token () ;
		tokens.token_val = c ;
		tokens.token = T_OPERATOR ;
		return (tokens.token) ;		// returns the Token for Arithmetic Operators
	}

	if (c == EOF){         			// End Of Archive detection for enhanced Batch Processing
        exit (0) ;
    }

	update_old_token () ;
	tokens.token = c ;
	return (tokens.token) ;		// returns a literal
}


void rd_syntax_error (int expected, int token, char *output)
{
	fprintf (stderr, "ERROR in line %d ", line_counter) ;
	fprintf (stderr, output, expected, token) ;

	exit (0) ;
}


void MatchSymbol (int expected_token)
{
	if (tokens.token != expected_token) {
		rd_syntax_error (expected_token, tokens.token, "token %d expected, but %d was read") ;
		exit (0) ;
	} else {
	 	rd_lex () ; /// read next Token
	}
}


// #define ParseLParen() 	MatchSymbol ('(') ; // More concise and efficient definitions
// #define ParseRParen() 	MatchSymbol (')') ; ///   rather than using functions
											/// The actual recomendation is to use MatchSymbol in the code rather than theese macros


void ParseYourGrammar (void)
{
  ParseExpression();
}


void ParseAxiom (void)
{
	ParseYourGrammar ();
    printf("\n");

	if (tokens.token == '\n') {
		MatchSymbol ('\n');
	}
    else {
		rd_syntax_error (-1, tokens.token, "-- Token inesperado (Expected:%d=None, Read:%d) al final del Parsing\n") ;
	}
}


void ParseExpression(void)
{
	/**
	* Number
    * This part of the code evals is the actual token is a number so it consums it in the
	* MatchSymbol function
    */
	if (tokens.token == T_NUMBER) {
		printf("%d", tokens.number);
		MatchSymbol(T_NUMBER);
	}

	/**
	* Variable
	* This part of the code evals is the actual token is a variable so it consums it in the
	* MatchSymbol function
	*/
	else if (tokens.token == T_VARIABLE) { // Evalue si el token es una variable
		printf("%s", tokens.variable_name);
		MatchSymbol(T_VARIABLE);
	}

	/**
	* Operator
	* This part of the code evals is the actual token is a number so it consums it in the
	* MatchSymbol function
	*/
	else if (tokens.token == T_OPERATOR || tokens.token == '=') {
		char op = tokens.token_val;
		int asignacion = (tokens.token == '=');
		MatchSymbol(tokens.token); // We get the next token
		/**
		* Everytime that an operator is the actual token a "(" has to be printed.
		* This is due to the structure of our grammar
        */
		printf("(");
		ParseExpression(); // As we have a new token, we call again this function

		if (asignacion) {
			printf(" = ");
		} else {
			printf(" %c ", op);
		}

		// In the case that the expresion has ended and a ")" has to be written
		if (tokens.token == ')' || tokens.token == '\n') {
			rd_syntax_error(0, tokens.token, "Falta un operando en la expresión\n");
		}

		ParseExpression();
		printf(")"); // We end the expression
	}

	/**
	* Parenthesis
	* Evals if the actual token is a "(" so it consums it and calls the function again waiting for the
	* other parenthesis to arrive
	*/
	else if (tokens.token == '(') {
		MatchSymbol('(');
		//Verificamos que después de un `(` no haya otro `(`
		if (tokens.token == '(') {
			rd_syntax_error(0, tokens.token, "Paréntesis redundantes detectados\n");
		}
		ParseExpression();
		MatchSymbol(')');
	}

	else {
		rd_syntax_error(0, tokens.token, "Token inesperado en la expresión: %d\n");
	}
}


int main (int argc, char **argv)
{
// Usage :  drLL -s  ==> evaluate a single Input Line
//          drLL     ==> evalute multiple Input Lines until some error appears
/// DO NOT MODIFY THE CODE INSIDE THE MAIN FUNCTION WITHOUT PERMISSION

	int flagMultiple = 1 ;

	if (argc >= 2) {
		if (strcmp ("-s", argv [1]) == 0) {
			flagMultiple = 0 ;
		}
	}

	rd_lex () ;	 /// Read first Token only once
	do {
		ParseAxiom () ;
	} while (flagMultiple) ;

	exit (0) ;
}
