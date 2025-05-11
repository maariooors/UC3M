# Variables
BISON = bison
GCC = gcc
CFLAGS = -Wall -g

# Inputs and outputs for trad
BISON_INPUT_TRAD = trad.y
BISON_OUTPUT_TRAD = trad.tab.c
REMOVE_HEADER_TRAD = trad.tab.h
EXEC_TRAD = trad

# Inputs and outputs for back
BISON_INPUT_BACK = back.y
BISON_OUTPUT_BACK = back.tab.c
REMOVE_HEADER_BACK = back.tab.h
EXEC_BACK = back

# Default target
all: $(EXEC_TRAD) $(EXEC_BACK)

# Target to generate the Bison output for trad
$(BISON_OUTPUT_TRAD): $(BISON_INPUT_TRAD)
	$(BISON) -d $(BISON_INPUT_TRAD) -o $(BISON_OUTPUT_TRAD)

# Target to generate the Bison output for back
$(BISON_OUTPUT_BACK): $(BISON_INPUT_BACK)
	$(BISON) -d $(BISON_INPUT_BACK) -o $(BISON_OUTPUT_BACK)

# Link the object files and generate the executable for trad
$(EXEC_TRAD): $(BISON_OUTPUT_TRAD)
	$(GCC) $(BISON_OUTPUT_TRAD) -o $(EXEC_TRAD)

# Link the object files and generate the executable for back
$(EXEC_BACK): $(BISON_OUTPUT_BACK)
	$(GCC) $(BISON_OUTPUT_BACK) -o $(EXEC_BACK)

# Clean up build files
clean:
	rm -f $(EXEC_TRAD) $(BISON_OUTPUT_TRAD) $(REMOVE_HEADER_TRAD)
	rm -f $(EXEC_BACK) $(BISON_OUTPUT_BACK) $(REMOVE_HEADER_BACK)