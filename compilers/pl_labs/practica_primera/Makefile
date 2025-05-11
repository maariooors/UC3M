# Variables
CC = gcc
CFLAGS = -Wall -g
EXEC = drLL
SRC = drLL.c

# Default target
all: $(EXEC)

# Compile the source file
$(EXEC): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(EXEC)

# Clean up build files
clean:
	rm -f $(EXEC)