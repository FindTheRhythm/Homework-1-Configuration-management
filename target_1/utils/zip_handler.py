import os
import zipfile


def extract_zip(zip_path, extract_to="vfs_temp"):
    """
    Распаковывает архив zip в указанную директорию.
    Если директория уже существует, она сначала очищается.
    """
    if not zipfile.is_zipfile(zip_path):
        
    # Удаляем предыдущую директорию, если она существует
    if os.path.exists(extract_to):
       
    # Распаковка архива
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    return os.path.abspath(extract_to)
