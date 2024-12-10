-include ../Makefile.defaults

compile:
	dotnet new console -o build -n build --force
	cp Program.cs build/Program.cs
	dotnet build build/ -c Release --no-incremental

clean:
	dotnet clean

measure:
ifndef JSON
	$(error No JSON defined.)
else ifndef ARGS
	$(error No ARGS defined.)
endif
	@../../../RAPL/build/rapl --json "$(JSON)" dotnet run -c Release --project build/ --no-build -- $(ARGS)

command:
ifndef ARGS
	$(error No ARGS defined.)
endif
	@echo dotnet run -c Release --project build/ --no-build -- $(ARGS)
