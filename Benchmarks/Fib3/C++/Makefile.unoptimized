-include ../Makefile.defaults

compile:
	g++ fib3.cpp -o fib3 -O3

clean:
	rm fib3

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" ./fib3 $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo ./fib3 $(ARGS)