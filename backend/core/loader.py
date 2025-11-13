from pathlib import Path

class ResumeLoader:
    """Handles loading of resume text files."""

    @staticmethod
    def load_text(file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path.read_text(encoding="utf-8")
