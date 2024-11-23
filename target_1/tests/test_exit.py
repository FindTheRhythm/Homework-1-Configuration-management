import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shell_commands import Shell
from utils.logger import Logger

class TestExit(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("test_log.json")
        self.shell = Shell("testhost", ".", self.logger)

    def test_exit_command(self):
        # Симулируем выполнение команды "exit"
        result = self.shell.execute_command("exit")
        # Проверяем, что выполнение завершилось (возвращает False)
        self.assertFalse(result)

    def test_log_saving_on_exit(self):
        self.shell.execute_command("ls")
        self.shell.execute_command("exit")
        with open(self.logger.logfile, "r") as log_file:
            logs = log_file.read()
        self.assertIn("ls", logs)

if __name__ == "__main__":
    unittest.main()
