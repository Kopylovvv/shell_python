import pytest
from unittest.mock import Mock, patch


from core import ShellCore  # замените your_module на актуальный путь


class TestShellCore:
    """Тесты для ядра shell"""

    @pytest.fixture
    def mock_logger(self):
        """Фикстура для создания мок-логгера"""
        mock_logger = Mock()
        mock_logger.info = Mock()
        return mock_logger

    @pytest.fixture
    def shell_core(self, mock_logger):
        """Фикстура для создания экземпляра ShellCore с мок-логгером"""
        return ShellCore(mock_logger)

    @pytest.fixture
    def mock_command(self):
        """Фикстура для создания мок-команды"""
        mock_cmd = Mock()
        mock_cmd.name = "test_command"
        mock_cmd.execute = Mock()
        return mock_cmd

    def test_execute_existing_command_successfully(self, shell_core, mock_command, mock_logger):
        """Тест: успешное выполнение существующей команды"""
        # Регистрируем мок-команду в shell
        shell_core.register_command(mock_command)

        # Выполняем команду
        shell_core.execute_command("test_command arg1 arg2 -o\n")

        # Проверяем, что команда была вызвана с правильными аргументами
        mock_command.execute.assert_called_once_with(["arg1", "arg2"], ["o"])

        # Проверяем, что команда была залогирована
        mock_logger.info.assert_called_with("test_command arg1 arg2 -o")

    def test_execute_empty_command_does_nothing(self, shell_core, mock_logger):
        """Тест: выполнение пустой команды просто выводит пустую строку"""
        # Мокаем print для проверки вывода
        with patch('builtins.print') as mock_print:
            shell_core.execute_command("\n")

            # Проверяем, что была вызвана пустая строка
            mock_print.assert_called_once_with()

            # Проверяем, что логирование не вызывалось для пустой команды
            mock_logger.info.assert_not_called()

    def test_execute_command_with_only_newline(self, shell_core, mock_logger):
        """Тест: выполнение команды состоящей только из переноса строки"""
        with patch('builtins.print') as mock_print:
            shell_core.execute_command("\n")

            # Проверяем, что была вызвана пустая строка
            mock_print.assert_called_once_with()

            # Проверяем, что логирование не вызывалось
            mock_logger.info.assert_not_called()

    def test_register_command(self, shell_core, mock_command):
        """Тест: регистрация команды в shell"""
        # Регистрируем команду
        shell_core.register_command(mock_command)

        # Проверяем, что команда добавлена в словарь
        assert "test_command" in shell_core.commands
        assert shell_core.commands["test_command"] == mock_command

