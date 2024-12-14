-include ../Makefile.defaults

compile:
	cargo build --release

clean:
	cargo clean

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" ./target/release/setsort $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo ./target/release/setsort $(ARGS)
