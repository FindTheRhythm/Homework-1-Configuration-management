import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shell_commands import Shell
from utils.logger import Logger

class TestMV(unittest.TestCase):
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

    def test_mv_file(self):
        src_file = os.path.join(self.test_dir, "test.txt")
        dest_file = os.path.join(self.test_dir, "renamed.txt")
        with open(src_file, "w") as f:
            f.write("test content")
        self.shell.mv(["test.txt", "renamed.txt"])
        self.assertTrue(os.path.exists(dest_file))
        self.assertFalse(os.path.exists(src_file))

    def test_mv_directory(self):
        src_dir = os.path.join(self.test_dir, "testdir")
        dest_dir = os.path.join(self.test_dir, "renameddir")
        os.mkdir(src_dir)
        self.shell.mv(["testdir", "renameddir"])
        self.assertTrue(os.path.exists(dest_dir))
        self.assertFalse(os.path.exists(src_dir))

    def test_mv_nonexistent_file(self):
        self.shell.mv(["nonexistent.txt", "renamed.txt"])
        self.assertFalse(os.path.exists("renamed.txt"))

if __name__ == "__main__":
    unittest.main()
