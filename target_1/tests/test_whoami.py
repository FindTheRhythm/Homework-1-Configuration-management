import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shell_commands import Shell
from utils.logger import Logger

class TestWhoami(unittest.TestCase):
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

    def test_whoami_output(self):
        import getpass
        expected_user = getpass.getuser()
        self.shell.whoami()
        last_log = self.logger.logs[-1]
        self.assertEqual(last_log["result"], expected_user)

if __name__ == "__main__":
    unittest.main()
