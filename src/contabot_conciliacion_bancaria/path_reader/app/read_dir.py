from pathlib import Path


class ReadDir:

    @staticmethod
    def execute(dir_path: Path, pattern: str) -> tuple[Path, ...]:
        """
        Execute the reading of files in a directory with a specific pattern.

        Args:
            dir_path (str): The path to the directory to read.
            pattern (str): The pattern to filter by (e.g., '*.txt').
        """
        files: tuple[Path, ...] = tuple(dir_path.rglob(pattern, case_sensitive=False))
        if not files:
            return tuple()

        directories = set()
        for file_path in files:
            if file_path.is_file():
                directories.add(file_path.parent)
        return tuple(directories)
