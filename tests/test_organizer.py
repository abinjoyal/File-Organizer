import tempfile
import unittest
from pathlib import Path
from file_organizer.organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)
        self.organizer = FileOrganizer()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_organization(self):
        # Create dummy files
        img_file = self.test_path / "test_image.png"
        doc_file = self.test_path / "test_doc.pdf"
        unknown_file = self.test_path / "test_file.xyz"

        img_file.touch()
        doc_file.touch()
        unknown_file.touch()

        # Run organizer
        moved_count, _ = self.organizer.organize(self.test_path)

        self.assertEqual(moved_count, 3)
        self.assertTrue((self.test_path / "Images" / "test_image.png").exists())
        self.assertTrue((self.test_path / "Documents" / "test_doc.pdf").exists())
        self.assertTrue((self.test_path / "Others" / "test_file.xyz").exists())

    def test_dry_run(self):
        img_file = self.test_path / "test_image.png"
        img_file.touch()

        moved_count, _ = self.organizer.organize(self.test_path, dry_run=True)

        self.assertEqual(moved_count, 1)
        # Original file should still be at root, not moved in dry-run
        self.assertTrue(img_file.exists())
        self.assertFalse((self.test_path / "Images" / "test_image.png").exists())


if __name__ == "__main__":
    unittest.main()
