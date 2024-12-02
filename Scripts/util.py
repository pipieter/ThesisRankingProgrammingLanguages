import os


def verify_dir(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)
