# Variables
BISON = bison
GCC = gcc
BISON_INPUT = calc6.y
BISON_OUTPUT = calc6.tab.c
REMOVE_HEADER = calc6.tab.h
EXEC = calc6
CFLAGS = -Wall -g

# Default target
all: $(EXEC)

# Target to generate the Bison output
$(BISON_OUTPUT): $(BISON_INPUT)
	$(BISON) -d $(BISON_INPUT) -o $(BISON_OUTPUT)

# Link the object files and generate the executable using gcc
$(EXEC): $(BISON_OUTPUT)
	$(GCC) $(BISON_OUTPUT) -o $(EXEC)

# Clean up build files
clean:
	rm -f $(EXEC) $(BISON_OUTPUT) $(REMOVE_HEADER)
