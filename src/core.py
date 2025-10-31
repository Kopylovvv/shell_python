import importlib
from pathlib import Path

from commands.base import BaseCommand
from src.utils.error_decorator import error_handler
from src.utils.logger import get_logger
from src.utils.parser import parse_object

logger = get_logger(Path(__file__).parent.parent / "shell.log")


class ShellCore:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.commands = {}

    def register_command(self, command: BaseCommand):
        """
        добавление команды в словарь ядра с командами
        Args:
            command (BaseCommand): класс команды унаследованный от BaseCommand
        """
        self.commands[command.name] = command

    def auto_discover_commands(self, commands_folder : str = "commands"):
        """
        автоматически находит и добавляет все команды из папки commands кроме base.py в словарь с командами
        Args:
            commands_folder (str): путь до папки с командами
        """
        commands_dir = Path(__file__).parent / commands_folder # путь к папке с командами
        commands_path = Path(commands_dir) # создание универсального пути для любой ос

        for file_path in commands_path.iterdir(): # итерация по файлам в директории
            # проверка, что это Python файл и не абстрактный класс или __init__.py
            if file_path.suffix == ".py" and file_path.name not in ["__init__.py", "base.py"]:
                module_name = file_path.stem  # имя модуля без расширения

                # импот модуля команды
                module = importlib.import_module(f".{module_name}", package=commands_folder)

                # поиск всех классы в модуле, которые являются командами
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    # проверка на класс, наследование от абстрактного класса и что это не он
                    if isinstance(attr, type) and issubclass(attr, BaseCommand) and attr != BaseCommand:
                        command_instance = attr()
                        self.register_command(command_instance) # добавление в словарь

    @error_handler(logger) # декоратор для логирования ошибок
    def execute_command(self, command: str):
        """
        функция которая выполняет команду поданную на вход:
        1) парсинг строки на имя команды, аргументы и флаги
        2) проверка на наличие команды в словаре
        3) логирование о выполнении данной команды
        4) выполнение команды через функцию класса команды
        если команды нет в словаре, то сообщение об ошибке
        Args:
            command (str): строка с командой
        """
        command_params = parse_object(command)

        if command_params["command_name"] in self.commands:
            logger.info(command[:-1])
            self.commands[command_params["command_name"]].execute(command_params["arguments"], command_params["options"])
        elif command_params["command_name"] == '':
            print()
        else:
            logger.info(command[:-1])
            raise SyntaxError(f"{command_params["command_name"]}: unknown command")
