from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Notification:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def has_errors(self) -> bool:
        return bool(self.errors)

    def has_warnings(self) -> bool:
        return bool(self.warnings)

    def add_error(self, message: str):
        self.errors.append(message)

    def add_warning(self, messages: str):
        for message in messages.split("\r"):
            self.warnings.append(message)

    def create_file(self, store_dir: Path) -> None:
        if not self.has_errors() and not self.has_warnings():
            return

        file_path = store_dir.parent / f"{store_dir.stem} observacion.txt"

        errors = "Errors:\n" + "\n".join(f"- {error}" for error in self.errors)
        warnings = "Warnings:\n" + "\n".join(
            f"- {warning}" for warning in self.warnings
        )
        file_path.write_text(f"{errors}\n{warnings}")
