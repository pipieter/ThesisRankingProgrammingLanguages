-include ../Makefile.defaults

compile:
	javac -d . PageRank.java

clean:
	rm PageRank

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" java PageRank $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo java PageRank $(ARGS)