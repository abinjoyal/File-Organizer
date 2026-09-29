import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from .rules import RuleManager
from .undo import UndoManager
from .utils import (
    setup_logger,
    get_unique_destination,
    format_bytes,
    get_file_date_subfolder,
    is_messy_filename,
    generate_clean_filename,
    extract_archive
)


class FileOrganizer:
    """Enhanced FileOrganizer supporting Undo recording, Date sorting, Smart renaming, and Auto-unzip."""

    def __init__(self, config_path: Optional[Path] = None, logger=None):
        self.rule_manager = RuleManager(config_path=config_path)
        self.logger = logger or setup_logger()
        self.undo_manager = UndoManager(logger=self.logger)

    def organize(
        self,
        target_directory: Path,
        dry_run: bool = False,
        date_sort: bool = False,
        unzip: bool = False,
        clean_names: bool = False
    ) -> Tuple[int, int]:
        """
        Organize files in target_directory into categorized folders.
        
        :param target_directory: Directory to organize
        :param dry_run: If True, simulates moves without touching disk
        :param date_sort: If True, organizes into Category/YYYY/MonthName/
        :param unzip: If True, extracts .zip archive files into subfolders
        :param clean_names: If True, renames UUID/hash filenames to clean indexed names
        :return: Tuple of (moved_count, total_bytes)
        """
        target = Path(target_directory).resolve()

        if not target.exists() or not target.is_dir():
            self.logger.error(f"Target path '{target}' is not a valid directory.")
            return 0, 0

        mode_str = "[DRY RUN] " if dry_run else ""
        self.logger.info(f"{mode_str}Starting file organization in: {target}")

        moved_count = 0
        total_bytes = 0
        session_moves: List[Dict[str, str]] = []

        category_names = set(self.rule_manager.categories.keys()).union({"Others", "Duplicates"})

        clean_counters: Dict[str, int] = {}

        for item in target.iterdir():
            # Skip directories, category subfolders, logs, hidden files
            if item.is_dir() or item.name.startswith(".") or item.name in category_names:
                continue

            try:
                file_size = item.stat().st_size
                category = self.rule_manager.get_category(item.suffix)

                # Determine target subfolder (Date sort vs standard)
                if date_sort:
                    date_sub = get_file_date_subfolder(item)
                    dest_dir = target / category / date_sub
                else:
                    dest_dir = target / category

                # Handle smart clean renaming for messy UUIDs/hashes
                filename = item.name
                if clean_names and is_messy_filename(filename):
                    clean_counters[category] = clean_counters.get(category, 0) + 1
                    filename = generate_clean_filename(category, item.name, clean_counters[category])

                dest_path = get_unique_destination(dest_dir, filename)

                if dry_run:
                    self.logger.info(f"[SIMULATION] Would move '{item.name}' -> '{dest_path.relative_to(target)}' ({format_bytes(file_size)})")
                else:
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(dest_path))
                    self.logger.info(f"Moved '{item.name}' -> '{dest_path.relative_to(target)}' ({format_bytes(file_size)})")

                    # Record transaction for undo
                    session_moves.append({
                        "source": str(item.resolve()),
                        "destination": str(dest_path.resolve())
                    })

                    # Handle auto-unzip if archive and requested
                    if unzip and category == "Archives" and dest_path.suffix.lower() == ".zip":
                        extract_folder = dest_dir / dest_path.stem
                        self.logger.info(f"📦 Extracting archive '{dest_path.name}' -> '{extract_folder.relative_to(target)}'")
                        extract_archive(dest_path, extract_folder)

                moved_count += 1
                total_bytes += file_size

            except Exception as e:
                self.logger.error(f"Failed to process '{item.name}': {e}")

        if not dry_run and session_moves:
            self.undo_manager.record_session(session_moves)

        summary = f"{mode_str}Completed! Processed {moved_count} file(s) ({format_bytes(total_bytes)})."
        self.logger.info(summary)

        return moved_count, total_bytes
