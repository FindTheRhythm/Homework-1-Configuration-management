import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shell_commands import Shell
from utils.logger import Logger

class TestLS(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("test_log.json")
        self.shell = Shell("testhost", os.getcwd(), self.logger)

    def test_ls_current_dir(self):
        result = self.shell.ls()
        self.assertTrue(result)
        self.assertIn("shell_commands.py", os.listdir())

if __name__ == "__main__":
    unittest.main()
