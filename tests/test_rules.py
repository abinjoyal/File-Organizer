import unittest
from file_organizer.rules import RuleManager


class TestRuleManager(unittest.TestCase):

    def setUp(self):
        self.rule_manager = RuleManager()

    def test_image_extensions(self):
        self.assertEqual(self.rule_manager.get_category(".jpg"), "Images")
        self.assertEqual(self.rule_manager.get_category(".PNG"), "Images")

    def test_document_extensions(self):
        self.assertEqual(self.rule_manager.get_category(".pdf"), "Documents")
        self.assertEqual(self.rule_manager.get_category(".txt"), "Documents")

    def test_code_extensions(self):
        self.assertEqual(self.rule_manager.get_category(".py"), "Code")
        self.assertEqual(self.rule_manager.get_category(".js"), "Code")

    def test_unknown_extension(self):
        self.assertEqual(self.rule_manager.get_category(".unknownext"), "Others")
        self.assertEqual(self.rule_manager.get_category(""), "Others")


if __name__ == "__main__":
    unittest.main()
