-include ../Makefile.defaults

compile:
	g++ pagerank.cpp -o pagerank -O3

clean:
	rm pagerank

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" ./pagerank $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo ./pagerank $(ARGS)