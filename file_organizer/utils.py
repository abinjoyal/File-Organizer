import re
import logging
import zipfile
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logger(log_dir: Path = None) -> logging.Logger:
    """Set up logger for file operations, outputting to console and log file."""
    logger = logging.getLogger("FileOrganizer")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_dir is None:
        log_dir = Path(__file__).resolve().parent.parent / "logs"

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "organizer.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Failed to set up file logging: {e}")

    return logger


def get_unique_destination(target_dir: Path, filename: str) -> Path:
    """Generate a non-conflicting path in target_dir for filename by appending (1), (2), etc."""
    dest_path = target_dir / filename
    if not dest_path.exists():
        return dest_path

    path_obj = Path(filename)
    stem = path_obj.stem
    suffix = path_obj.suffix
    counter = 1

    while dest_path.exists():
        dest_path = target_dir / f"{stem}({counter}){suffix}"
        counter += 1

    return dest_path


def format_bytes(size: int) -> str:
    """Format byte size into human readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def get_file_date_subfolder(file_path: Path) -> Path:
    """Return Path(YYYY/MonthName) based on file modification time."""
    try:
        mtime = file_path.stat().st_mtime
        dt = datetime.fromtimestamp(mtime)
        return Path(str(dt.year)) / dt.strftime("%B")
    except Exception:
        return Path("Unknown_Date")


def is_messy_filename(filename: str) -> bool:
    """Detect if a filename looks like a hex hash or UUID (e.g. 00ab9670869...jpg or UUID format)."""
    stem = Path(filename).stem
    # Match UUID hex pattern (32+ hex chars or dashes)
    uuid_pattern = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    hex_pattern = re.compile(r"^[0-9a-fA-F]{24,}$")
    return bool(uuid_pattern.match(stem) or hex_pattern.match(stem))


def generate_clean_filename(category: str, original_filename: str, index: int) -> str:
    """Generate a clean, structured filename like Image_20260927_001.jpg."""
    suffix = Path(original_filename).suffix
    date_str = datetime.now().strftime("%Y%m%d")
    category_prefix = category.rstrip("s")  # Images -> Image, Documents -> Document
    return f"{category_prefix}_{date_str}_{index:03d}{suffix}"


def extract_archive(archive_path: Path, extract_to_dir: Path) -> bool:
    """Safely extract archive file (.zip, .tar, .gz) into extract_to_dir."""
    try:
        extract_to_dir.mkdir(parents=True, exist_ok=True)
        if archive_path.suffix.lower() == ".zip":
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(extract_to_dir)
            return True
        elif archive_path.suffix.lower() in [".tar", ".gz", ".tgz"]:
            with tarfile.open(archive_path, "r:*") as tar_ref:
                tar_ref.extractall(extract_to_dir)
            return True
    except Exception as e:
        logging.getLogger("FileOrganizer").error(f"Failed to extract '{archive_path.name}': {e}")
    return False
