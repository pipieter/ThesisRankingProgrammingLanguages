-include ../Makefile.defaults

compile:
	g++ ionumber.cpp -o ionumber -O3

clean:
	rm ionumber

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" ./ionumber $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo ./ionumber $(ARGS)