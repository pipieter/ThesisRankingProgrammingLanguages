-include ../Makefile.defaults

# PyPy reuses the Python files

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
	@../../../RAPL/build/rapl --json "$(JSON)" pypy3 ../Python/merge_sort.py $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo pypy3 ../Python/merge_sort.py $(ARGS)