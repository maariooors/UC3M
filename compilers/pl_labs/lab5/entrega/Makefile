# Variables
BISON = bison
FLEX = flex
GCC = gcc
CFLAGS = -Wall -g

calc51: calc51.tab.c
	$(GCC) $(CFLAGS) -o $@ $^

calc51.tab.c: calc51.y
	$(BISON) -d -o $@ $<

calc52: calc52.tab.c lex.yy.c
	$(GCC) $(CFLAGS) -o $@ lex.yy.c calc52.tab.c

calc52.tab.c: calc52.y
	$(BISON) -d -o $@ $<

lex.yy.c: calc52.lex
	$(FLEX) -o $@ $<

clean:
	rm -f calc51 calc52 calc51.tab.c calc51.tab.h calc52.tab.c calc52.tab.h lex.yy.c
