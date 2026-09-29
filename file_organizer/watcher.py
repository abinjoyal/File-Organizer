import time
import logging
from pathlib import Path
from typing import Optional


class DirectoryWatcher:
    """Monitors a directory in real-time and organizes new files as they arrive."""

    def __init__(self, organizer, target_dir: Path, poll_interval: int = 5, logger: Optional[logging.Logger] = None):
        self.organizer = organizer
        self.target_dir = Path(target_dir).resolve()
        self.poll_interval = poll_interval
        self.logger = logger or logging.getLogger("FileOrganizer")
        self._running = False

    def start(self, date_sort: bool = False, unzip: bool = False, clean_names: bool = False):
        """Start monitoring directory using polling loop or watchdog."""
        self.logger.info(f"👀 Live Watcher started for: {self.target_dir}")
        self.logger.info(f"Polling every {self.poll_interval}s. Press Ctrl+C to stop.")
        self._running = True

        try:
            while self._running:
                # Trigger single organization pass
                moved_count, _ = self.organizer.organize(
                    target_directory=self.target_dir,
                    dry_run=False,
                    date_sort=date_sort,
                    unzip=unzip,
                    clean_names=clean_names
                )
                if moved_count > 0:
                    self.logger.info(f"✨ Auto-sorted {moved_count} new file(s).")
                
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            self.logger.info("Live Watcher stopped by user.")
        except Exception as e:
            self.logger.error(f"Watcher encountered error: {e}")

    def stop(self):
        """Stop the monitoring loop."""
        self._running = False
