import sys
from pathlib import Path

from utils.console_info import get_info
from src.core import ShellCore
from utils.logger import get_logger


def run():
    """
    главная функция которая запускает ядро, логгер и принимает ввод
    """
    # инициализация логера и сообщение о старте
    logger = get_logger(Path(__file__).parent.parent / "shell.log")
    logger.info("start")

    # инициализация ядра и поиск доступных команд
    core = ShellCore()
    core.auto_discover_commands()

    # основной цикл в котором считывается команда и передается в ядро
    try:
        print(f"{get_info()}", end=' ') # приглашение командного интерпретатора
        for line in sys.stdin:
            core.execute_command(line) # выполнить команду из считанной строки
            print(f"{get_info()}", end=' ') # приглашение командного интерпретатора
    except KeyboardInterrupt:
        logger.info("exit")


if __name__ == "__main__":
    run()
