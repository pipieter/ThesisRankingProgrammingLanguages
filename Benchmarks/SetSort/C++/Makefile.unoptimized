-include ../Makefile.defaults

compile:
	g++ setsort.cpp -o setsort -O3

clean:
	rm setsort

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" ./setsort $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo ./setsort $(ARGS)