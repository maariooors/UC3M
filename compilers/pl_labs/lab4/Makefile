# Variables
BISON = bison
FLEX = flex
GCC = gcc
BISON_INPUT = calc4.y
BISON_OUTPUT = calc4.tab.c
BISON_HEADER = calc4.tab.h
FLEX_INPUT = calc4.lex
FLEX_OUTPUT = lex.yy.c
EXEC = calc4
CFLAGS = -Wall -g

# Default target
all: $(EXEC)

# Generate Bison output
$(BISON_OUTPUT) $(BISON_HEADER): $(BISON_INPUT)
	$(BISON) -d $(BISON_INPUT) -o $(BISON_OUTPUT)

# Generate Flex output
$(FLEX_OUTPUT): $(FLEX_INPUT)
	$(FLEX) $(FLEX_INPUT)

# Compile and link
$(EXEC): $(FLEX_OUTPUT) $(BISON_OUTPUT)
	$(GCC) $(FLEX_OUTPUT) $(BISON_OUTPUT) -o $(EXEC) -lm

# Clean up build files
clean:
	rm -f $(EXEC) $(BISON_OUTPUT) $(BISON_HEADER) $(FLEX_OUTPUT)
