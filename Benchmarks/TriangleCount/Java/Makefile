-include ../Makefile.defaults

compile:
	javac -d . TriangleCount.java

clean:
	rm TriangleCount

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" java TriangleCount $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo java TriangleCount $(ARGS)