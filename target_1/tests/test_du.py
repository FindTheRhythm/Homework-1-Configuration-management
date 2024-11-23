import unittest
import os
import sys
import tempfile
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shell_commands import Shell
from utils.logger import Logger

class TestDU(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()  # Создаем временную директорию
        self.logfile = os.path.join(self.test_dir, "test_log.json")  # Создаем временный файл для логов
        self.logger = Logger(logfile=self.logfile)  # Инициализируем логгер с указанием пути к файлу
        self.hostname = "myhost"  # Задаем имя компьютера для оболочки
        self.shell = Shell(root_dir=self.test_dir, logger=self.logger, hostname=self.hostname)  # Подключаем логгер и hostname к оболочке

    def tearDown(self):
        shutil.rmtree(self.test_dir)  # Удаляем временную директорию

    def test_du_empty_directory(self):
        # Создаем пустую директорию
        empty_dir = os.path.join(self.test_dir, "empty_dir")
        os.makedirs(empty_dir, exist_ok=True)

        # Выполняем команду du
        result = self.shell.du("empty_dir")
        self.assertEqual(result, {"size": 0})  # Ожидаем размер 0

        # Проверяем запись в логах
        log_entry = self.logger.logs[-1]
        self.assertEqual(log_entry["command"], "du empty_dir")
        self.assertEqual(log_entry["result"], {"size": 0})

    def test_du_file_size(self):
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("content")
        result = self.shell.du("test.txt")
        self.assertTrue(result)

    def test_du_directory_size(self):
        # Создаем директорию и файл
        test_dir = os.path.join(self.test_dir, "test_dir")
        os.makedirs(test_dir, exist_ok=True)
        file_path = os.path.join(test_dir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("1234567890")  # Размер файла 10 байт

        # Выполняем команду du
        result = self.shell.du("test_dir")
        self.assertEqual(result, {"size": 10})  # Ожидаем размер 10 байт

        # Проверяем запись в логах
        log_entry = self.logger.logs[-1]
        self.assertEqual(log_entry["command"], "du test_dir")
        self.assertEqual(log_entry["result"], {"size": 10})

    def test_du_empty_list(self):
        with self.assertRaises(ValueError) as context:
            self.shell.du([])  # Передаем пустой список
        self.assertEqual(str(context.exception), "Path cannot be an empty list")

if __name__ == "__main__":
    unittest.main()
