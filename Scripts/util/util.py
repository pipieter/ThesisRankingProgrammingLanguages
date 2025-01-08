import os


def get_files(directory: str) -> list[str]:
    files = []
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            files.append(item)
    return files
