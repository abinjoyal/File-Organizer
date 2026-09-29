import hashlib
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from .utils import get_unique_destination


class DuplicateScanner:
    """Scans a directory for identical files using SHA-256 chunk hashing."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger("FileOrganizer")

    @staticmethod
    def calculate_hash(file_path: Path, chunk_size: int = 65536) -> str:
        """Calculate SHA-256 checksum of a file in memory-efficient chunks."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()

    def find_duplicates(self, target_dir: Path) -> Dict[str, List[Path]]:
        """
        Scans target_dir and returns dict mapping SHA-256 hash to list of duplicate file paths.
        Only returns entries with 2 or more files.
        """
        hash_map: Dict[str, List[Path]] = {}

        for item in target_dir.rglob("*"):
            if item.is_file() and not item.name.startswith("."):
                try:
                    file_hash = self.calculate_hash(item)
                    hash_map.setdefault(file_hash, []).append(item)
                except Exception as e:
                    self.logger.warning(f"Could not hash '{item.name}': {e}")

        # Filter to only hashes with duplicates (> 1 file)
        duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
        return duplicates

    def move_duplicates(self, target_dir: Path, dry_run: bool = False) -> Tuple[int, int]:
        """
        Finds duplicates in target_dir and moves secondary duplicate copies into 'Duplicates/' folder.
        Keeps the first file in place.
        Returns tuple of (duplicates_found, duplicates_moved).
        """
        duplicates = self.find_duplicates(target_dir)
        total_dup_count = sum(len(paths) - 1 for paths in duplicates.values())

        if not total_dup_count:
            self.logger.info("No duplicate files found.")
            return 0, 0

        dup_dir = target_dir / "Duplicates"
        moved_count = 0

        for file_hash, paths in duplicates.items():
            original = paths[0]
            duplicates_list = paths[1:]

            self.logger.info(f"Duplicate group (Original: '{original.name}'): {len(duplicates_list)} duplicate copy(ies)")

            for dup_file in duplicates_list:
                if dry_run:
                    self.logger.info(f"[SIMULATION] Would move duplicate '{dup_file.name}' -> 'Duplicates/'")
                    moved_count += 1
                else:
                    try:
                        dup_dir.mkdir(exist_ok=True)
                        dest_path = get_unique_destination(dup_dir, dup_file.name)
                        shutil.move(str(dup_file), str(dest_path))
                        self.logger.info(f"Moved duplicate '{dup_file.name}' -> 'Duplicates/{dest_path.name}'")
                        moved_count += 1
                    except Exception as e:
                        self.logger.error(f"Failed to move duplicate '{dup_file.name}': {e}")

        return total_dup_count, moved_count
