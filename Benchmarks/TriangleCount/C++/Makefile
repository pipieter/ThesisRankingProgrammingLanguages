-include ../Makefile.defaults

compile:
	g++ trianglecount.cpp -o trianglecount -O3

clean:
	rm trianglecount

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" ./trianglecount $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo ./trianglecount $(ARGS)