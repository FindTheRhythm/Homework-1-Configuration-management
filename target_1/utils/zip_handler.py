import os
import zipfile
import tempfile


def extract_zip(zip_path):
    """
    Извлекает содержимое ZIP-файла во временную директорию
    и возвращает путь к директории 'home' или корневой директории.
    """
    temp_dir = tempfile.mkdtemp()  # Создаем временную директорию

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Проверяем, существует ли папка 'home' внутри распакованного содержимого
    home_path = os.path.join(temp_dir, "home")
    if os.path.exists(home_path) and os.path.isdir(home_path):
        return home_path  # Возвращаем путь к 'home'

    return temp_dir  # Если 'home' не существует, возвращаем корневую директорию

