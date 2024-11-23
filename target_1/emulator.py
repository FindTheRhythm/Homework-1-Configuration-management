import argparse
import os
import json



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
    logger = Logger(args.logfile)

    # Инициализация оболочки
    shell = Shell(hostname=args.hostname, vfs_path=vfs_path, logger=logger)

    # Выполнение стартового скрипта (если указан)
    if args.script:
        with open(args.script, "r") as script_file:
            for command in script_file:
                shell.execute_command(command.strip())

    # Запуск CLI
    while True:
        try:
            command = input(f"{args.hostname} > ")
            if not shell.execute_command(command.strip()):
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
