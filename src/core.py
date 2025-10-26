import os
import importlib
from commands.base import BaseCommand
from src.utils.parser import parse_object


class ShellCore:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.commands = {}

    def register_command(self, command: BaseCommand):
        """добавление команды в ядро"""
        self.commands[command.name] = command

    def auto_discover_commands(self, commands_folder="commands"):
        """Автоматически находит и регистрирует все команды в папке"""
        commands_dir = os.path.join(os.path.dirname(__file__), commands_folder)

        for filename in os.listdir(commands_dir):
            if filename.endswith(".py") and filename not in ["__init__.py", "base.py"]:
                module_name = filename[:-3]  # убираем .py
                try:
                    # Импортируем модуль команды
                    module = importlib.import_module(f".{module_name}", package=commands_folder)

                    # Ищем все классы в модуле, которые являются командами
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)

                        if isinstance(attr, type) and issubclass(attr, BaseCommand) and attr != BaseCommand:
                            command_instance = attr()
                            self.register_command(command_instance)

                except ImportError as e:
                    print(f"Ошибка импорта {module_name}: {e}")

    def execute_command(self, command: str):
        """Парсит аргументы, находит и выполняет команду, логирует результат."""
        # 1. Запись в лог и историю (начало)
        # 2. Поиск команды по имени
        # 3. Вызов command_obj.execute(args, options)
        # 4. Обработка исключений (запись в лог)
        # 5. Запись в лог и историю (успех/ошибка)
        command_params = parse_object(command)
        if command_params["command_name"] in self.commands:
            self.commands[command_params["command_name"]].execute(command_params["arguments"], command_params["options"])
        else:
            print(f"Команда '{command_params["command_name"]}' не найдена")


