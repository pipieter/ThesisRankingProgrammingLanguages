-include ../Makefile.defaults

compile:
	@:

clean:
	@:

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" python3 fib3.py $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo python3 fib3.py $(ARGS)