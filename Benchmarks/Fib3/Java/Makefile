-include ../Makefile.defaults

compile:
	javac -d . Fib3.java

clean:
	rm Fib3.class

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" java Fib3 $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo java Fib3 $(ARGS)