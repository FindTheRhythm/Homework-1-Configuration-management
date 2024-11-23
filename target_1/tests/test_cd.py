import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shell_commands import Shell
from utils.logger import Logger

class TestCD(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("test_log.json")
        self.test_dir = os.path.abspath("test_vfs")
        os.makedirs(self.test_dir, exist_ok=True)
        self.shell = Shell("testhost", self.test_dir, self.logger)

    def tearDown(self):
        # Удаляем тестовую директорию
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_cd_valid_directory(self):
        sub_dir = os.path.join(self.test_dir, "subdir")
        os.mkdir(sub_dir)
        self.shell.cd(["subdir"])
        self.assertEqual(self.shell.current_dir, sub_dir)

    def test_cd_invalid_directory(self):
        self.shell.cd(["nonexistent"])
        self.assertNotEqual(self.shell.current_dir, "nonexistent")

    def test_cd_no_arguments(self):
        self.shell.cd([])
        self.assertEqual(self.shell.current_dir, self.test_dir)

if __name__ == "__main__":
    unittest.main()
