import argparse
import os
import json
from utils.zip_handler import extract_zip
from utils.logger import Logger
from shell_commands import Shell

def main():
    # Инициализация аргументов командной строки
    parser = argparse.ArgumentParser(description="Эмулятор shell.")
    parser.add_argument("--hostname", required=True, help="Имя компьютера.")
    parser.add_argument("--vfs", required=True, help="Путь к архиву виртуальной файловой системы (zip).")
    parser.add_argument("--logfile", required=True, help="Путь к лог-файлу (json).")
    parser.add_argument("--script", required=False, help="Путь к стартовому скрипту.")
    args = parser.parse_args()

    # Распаковка архива VFS
    vfs_path = extract_zip(args.vfs)

    # Инициализация логгера
    logger = Logger(logfile=args.logfile)

    # Инициализация оболочки
    shell = Shell(hostname=args.hostname, root_dir=vfs_path, logger=logger)  # root_dir вместо vfs_path

    # Выполнение стартового скрипта (если указан)
    if args.script:
        with open(args.script, "r") as script_file:
            for command in script_file:
                command = command.strip()
                if command:
                    shell.execute_command(command)

    # Запуск CLI
    while True:
        try:
            command = input(f"{args.hostname}:{os.path.basename(shell.current_dir)}$ ").strip()
            if command:
                if not shell.execute_command(command):
                    break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
