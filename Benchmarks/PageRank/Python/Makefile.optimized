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
	@../../../RAPL/build/rapl --json "$(JSON)" python3 pagerank.py $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo python3 pagerank.py $(ARGS)