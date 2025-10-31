import os
from pathlib import Path


def get_info() -> str:
    """
    функция для получения данных приглашения командного интерпретатора
    Returns:
        str: строка с данными об имени пользователя и устройства и о текущей директории
    """

    username = os.getlogin() # имя пользователя
    hostname = os.uname().nodename # имя устройства
    current_dir = Path.cwd() # текущая директория

    return f"{username}@{hostname} {str(current_dir).split('/')[-1]} #"

