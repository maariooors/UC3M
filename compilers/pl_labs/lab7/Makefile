# Variables
BISON = bison
FLEX = flex
GCC = gcc
BISON_INPUT = calc7.y
BISON_OUTPUT = calc7.tab.c
BISON_HEADER = calc7.tab.h
FLEX_INPUT = calc7.lex
FLEX_OUTPUT = lex.yy.c
EXEC = calc7
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
	$(GCC) $(FLEX_OUTPUT) $(BISON_OUTPUT) -o $(EXEC)

# Clean up build files
clean:
	rm -f $(EXEC) $(BISON_OUTPUT) $(BISON_HEADER) $(FLEX_OUTPUT)