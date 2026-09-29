import json
from pathlib import Path
from typing import Dict, List

DEFAULT_CATEGORIES: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".odt", ".rtf"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg", ".wma"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar", ".iso"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".java", ".cpp", ".c", ".cs", ".go", ".rs", ".php", ".sh", ".sql"]
}


class RuleManager:
    """Manages file categorization rules based on configuration."""

    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path(__file__).resolve().parent.parent / "config" / "categories.json"
        self.categories = self._load_categories()

    def _load_categories(self) -> Dict[str, List[str]]:
        """Load categories from JSON config file or fall back to defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Convert extensions to lowercase for consistency
                    return {cat: [ext.lower() for ext in exts] for cat, exts in data.items()}
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path} ({e}). Using default rules.")
        return DEFAULT_CATEGORIES

    def get_category(self, extension: str) -> str:
        """Return category name for a given file extension."""
        ext_clean = extension.lower().strip()
        if not ext_clean:
            return "Others"

        for category, extensions in self.categories.items():
            if ext_clean in extensions:
                return category
        return "Others"
