from pathlib import Path


def get_absolute_path(cwd: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    return (cwd / path).resolve()
