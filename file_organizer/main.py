import argparse
import sys
from pathlib import Path

from .organizer import FileOrganizer
from .undo import UndoManager
from .duplicates import DuplicateScanner
from .watcher import DirectoryWatcher


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Automated File Organizer v2.0 - Sort files, handle duplicates, undo actions, and launch GUI."
    )
    parser.add_argument(
        "-p", "--path",
        type=str,
        default=None,
        help="Path to the target directory to organize."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Simulate file moves without actually changing any files."
    )
    parser.add_argument(
        "-u", "--undo",
        action="store_true",
        help="Rollback the last organization session."
    )
    parser.add_argument(
        "--date-sort",
        action="store_true",
        help="Organize files into Date-based subfolders (Category/YYYY/Month)."
    )
    parser.add_argument(
        "--find-duplicates",
        action="store_true",
        help="Scan for SHA-256 duplicate files and move them to 'Duplicates/' folder."
    )
    parser.add_argument(
        "--unzip",
        action="store_true",
        help="Automatically extract .zip archives into subfolders."
    )
    parser.add_argument(
        "--clean-names",
        action="store_true",
        help="Rename messy UUID or hash filenames into clean indexed names."
    )
    parser.add_argument(
        "-w", "--watch",
        action="store_true",
        help="Start live background folder monitoring mode."
    )
    parser.add_argument(
        "-g", "--gui",
        action="store_true",
        help="Launch Desktop Graphical User Interface (GUI)."
    )
    parser.add_argument(
        "-c", "--config",
        type=str,
        default=None,
        help="Custom path to categories JSON configuration file."
    )
    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_args()

    # Launch GUI if requested
    if args.gui:
        from .gui import launch_gui
        launch_gui()
        return

    # Handle Undo option
    if args.undo:
        undo_mgr = UndoManager()
        undo_mgr.undo_last_session()
        return

    config_path = Path(args.config) if args.config else None
    organizer = FileOrganizer(config_path=config_path)

    # Handle path input
    if args.path:
        target_path = Path(args.path)
    else:
        print("=== 📁 Python File Organizer v2.0 ===")
        user_input = input("Enter target directory path (Press Enter for current directory): ").strip()
        target_path = Path(user_input) if user_input else Path.cwd()

    # Handle Watcher option
    if args.watch:
        watcher = DirectoryWatcher(organizer, target_path)
        watcher.start(date_sort=args.date_sort, unzip=args.unzip, clean_names=args.clean_names)
        return

    # Handle Duplicate scanning option
    if args.find_duplicates:
        dup_scanner = DuplicateScanner()
        dup_scanner.move_duplicates(target_path, dry_run=args.dry_run)

    # Run Standard Organization
    organizer.organize(
        target_directory=target_path,
        dry_run=args.dry_run,
        date_sort=args.date_sort,
        unzip=args.unzip,
        clean_names=args.clean_names
    )


if __name__ == "__main__":
    main()
