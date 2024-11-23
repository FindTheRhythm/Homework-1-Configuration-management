import os
import shutil

class Shell:
    def __init__(self, hostname, root_dir, logger):
        """
        Инициализация Shell.
        :param hostname: Имя хоста для приглашения к вводу.
        :param root_dir: Корневая директория виртуальной файловой системы.
        :param logger: Логгер для записи действий.
        """
        self.hostname = hostname
        self.root_dir = root_dir  # Инициализация root_dir
        self.current_dir = root_dir  # Текущая директория по умолчанию — корень
        self.logger = logger

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return True

        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            return self.ls()
        elif cmd == "cd":
            return self.cd(args)
        elif cmd == "exit":
            self.logger.save()
            return False
        elif cmd == "du":
            return self.du(args)
        elif cmd == "mv":
            return self.mv(args)
        elif cmd == "whoami":
            return self.whoami()
        else:
            print(f"Unknown command: {cmd}")
            return True

    def ls(self):
        
    def cd(self, args):
        
    def du(self, path=None):
        
    def mv(self, args):
        
    def whoami(self):
        
