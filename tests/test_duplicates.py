import tempfile
import unittest
from pathlib import Path
from file_organizer.duplicates import DuplicateScanner


class TestDuplicateScanner(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)
        self.scanner = DuplicateScanner()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_and_move_duplicates(self):
        # Create two identical files and one distinct file
        f1 = self.test_path / "file1.txt"
        f2 = self.test_path / "copy_file1.txt"
        f3 = self.test_path / "unique.txt"

        f1.write_text("identical content")
        f2.write_text("identical content")
        f3.write_text("different content")

        total_dup, moved = self.scanner.move_duplicates(self.test_path)

        self.assertEqual(total_dup, 1)
        self.assertEqual(moved, 1)
        self.assertTrue((self.test_path / "Duplicates" / "copy_file1.txt").exists())
        self.assertTrue(f1.exists())
        self.assertTrue(f3.exists())


if __name__ == "__main__":
    unittest.main()
