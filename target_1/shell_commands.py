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
                try:
            items = os.listdir(self.current_dir)
            print("\n".join(items))
            self.logger.log("ls", items)
            return True
        except Exception as e:
            print(f"Error: {e}")
            self.logger.log("ls", str(e))
            return True

    def cd(self, args):
                if not args:
            print("Usage: cd <directory>")
            return True
        path = os.path.join(self.current_dir, args[0])
        if os.path.isdir(path):
            self.current_dir = path
            self.logger.log("cd", f"Changed to {path}")
        else:
            print(f"No such directory: {args[0]}")
            self.logger.log("cd", f"No such directory: {args[0]}")
        return True
        
    def du(self, path=None):
        """
        Вычисляет размер указанного каталога или файла.
        Если path не указан, используется текущий каталог.
        """
        if path is None:
            path = self.current_dir
        elif isinstance(path, list):
            if len(path) > 0:
                path = path[0]
            else:
                raise ValueError("Path cannot be an empty list")
        elif not isinstance(path, str):
            raise ValueError(f"Invalid path type: {type(path)}. Expected str.")

        abs_path = os.path.join(self.root_dir, path)

        if not os.path.exists(abs_path):
            result = {"error": f"Path '{path}' does not exist."}
            self.logger.log(f"du {path}", result)
            return result

        if os.path.isfile(abs_path):
            size = os.path.getsize(abs_path)
            result = {"size": size}
            self.logger.log(f"du {path}", result)
            return result

        total_size = 0
        for dirpath, dirnames, filenames in os.walk(abs_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)

        result = {"size": total_size}
        self.logger.log(f"du {path}", result)
        return result
        
    def mv(self, args):
                if len(args) < 2:
            print("Usage: mv <source> <destination>")
            return True
        src, dest = args
        try:
            shutil.move(os.path.join(self.current_dir, src), os.path.join(self.current_dir, dest))
            print(f"Moved {src} to {dest}")
            self.logger.log("mv", f"Moved {src} to {dest}")
        except Exception as e:
            print(f"Error: {e}")
            self.logger.log("mv", str(e))
        return True
        
    def whoami(self):
        user = os.getlogin()
        print(user)
        self.logger.log("whoami", user)
        return True
