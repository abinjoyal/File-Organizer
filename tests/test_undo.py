import tempfile
import unittest
from pathlib import Path
from file_organizer.organizer import FileOrganizer
from file_organizer.undo import UndoManager


class TestUndoManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)

        self.history_file = self.test_path / "history.json"
        self.organizer = FileOrganizer()
        self.organizer.undo_manager = UndoManager(history_file=self.history_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_undo_restores_files(self):
        # Create test file
        test_file = self.test_path / "doc.pdf"
        test_file.write_text("sample content")

        # Organize file
        self.organizer.organize(self.test_path)
        self.assertFalse(test_file.exists())
        self.assertTrue((self.test_path / "Documents" / "doc.pdf").exists())

        # Undo session
        restored, failed = self.organizer.undo_manager.undo_last_session()

        self.assertEqual(restored, 1)
        self.assertEqual(failed, 0)
        self.assertTrue(test_file.exists())
        self.assertFalse((self.test_path / "Documents" / "doc.pdf").exists())


if __name__ == "__main__":
    unittest.main()
