-include ../Makefile.defaults

compile:
	javac -d . IONumber.java

clean:
	rm IONumber

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" java IONumber $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo java IONumber $(ARGS)