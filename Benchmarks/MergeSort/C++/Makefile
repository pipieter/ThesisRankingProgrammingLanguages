-include ../Makefile.defaults

compile:
	g++ merge_sort.cpp -o merge_sort -O3

clean:
	rm merge_sort

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" ./merge_sort $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo ./merge_sort $(ARGS)