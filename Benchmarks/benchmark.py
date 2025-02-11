import os.path
import subprocess


def get_command(
    language: str, optimized: bool, cwd: str, args: dict
) -> list[str] | None:
    makefile = os.path.join(cwd, f"Makefile.{language}")

    if optimized:
        result = subprocess.run(
            ["make", "-f", makefile, "command-optimized"],
            shell=False,
            cwd=cwd,
            env=args,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        # command-optimized not found, return None
        if result.returncode == 2:
            return None
        command = result.stdout.decode("utf-8")
    else:
        command = subprocess.check_output(
            ["make", "-f", makefile, "command"],
            shell=False,
            cwd=cwd,
            env=args,
        ).decode("utf-8")

    return command.strip().split(" ")
