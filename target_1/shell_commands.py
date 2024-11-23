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
        self.previous_dir = None
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
        elif cmd == "pwd":
            return self.pwd()
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

        if args[0] == "-":
            # Возврат в предыдущую директорию
            if self.previous_dir:
                self.current_dir, self.previous_dir = self.previous_dir, self.current_dir
                print(f"Changed to previous directory: {self.current_dir}")
                self.logger.log("cd", f"Changed to previous directory: {self.current_dir}")
            else:
                print("No previous directory to return to.")
                self.logger.log("cd", "No previous directory to return to.")
            return True

        path = os.path.join(self.current_dir, args[0])
        if os.path.isdir(path):
            self.previous_dir = self.current_dir  # Сохраняем текущую директорию
            self.current_dir = path
            self.logger.log("cd", f"Changed to {path}")
        else:
            print(f"No such directory: {args[0]}")
            self.logger.log("cd", f"No such directory: {args[0]}")
        return True

    def pwd(self):
        """
        Отображает текущую директорию.
        """
        relative_path = os.path.relpath(self.current_dir, self.root_dir)
        relative_path = "/" if relative_path == "." else f"/{relative_path.replace(os.sep, '/')}"
        print(relative_path)
        self.logger.log("pwd", {"current_dir": relative_path})
        return True

    def du(self, path=None):
        """
        Вычисляет размер указанного каталога или файла.
        Если path не указан, используется текущий каталог.
        """
        # Если path — это список, проверить его содержимое
        if isinstance(path, list):
            if len(path) > 0:
                path = path[0]  # Используем первый элемент
            else:
                path = "."  # По умолчанию текущая директория
        elif path is None:
            path = "."  # Если path не указан

        # Получение абсолютного пути
        abs_path = os.path.join(self.current_dir, path)

        # Проверка существования пути
        if not os.path.exists(abs_path):
            result = {"error": f"Path '{path}' does not exist."}
            self.logger.log(f"du {path}", result)
            print(result)  # Выводим ошибку в консоль
            return result

        try:
            # Если это файл, возвращаем его размер
            if os.path.isfile(abs_path):
                size = os.path.getsize(abs_path)
                result = {"size": size}
                self.logger.log(f"du {path}", result)
                print(result)  # Выводим результат в консоль
                return result

            # Если это директория, вычисляем общий размер
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(abs_path):
                for f in filenames:
                    try:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                    except (OSError, PermissionError) as e:
                        # Логируем недоступные файлы, но продолжаем
                        self.logger.log(f"Error accessing file: {fp}", {"error": str(e)})

            result = {"size": total_size}
            self.logger.log(f"du {path}", result)
            print(result)  # Выводим результат в консоль
            return result

        except Exception as e:
            result = {"error": f"An unexpected error occurred: {str(e)}"}
            self.logger.log(f"du {path}", result)
            print(result)  # Выводим ошибку в консоль
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