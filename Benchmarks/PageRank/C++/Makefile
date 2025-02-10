-include ../Makefile.defaults

CC := g++
CFLAGS := -O3
OUT := ./unoptimized

compile:
	$(CC) unoptimized.cpp -o $(OUT) $(CFLAGS)

clean:
	rm $(OUT)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo $(OUT) $(ARGS)