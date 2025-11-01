import pytest
from unittest.mock import patch

from commands.cat import CatCommand


class TestCatCommand:
    """Тесты для команды cat"""

    @pytest.fixture
    def command(self):
        """Фикстура для создания экземпляра команды"""
        return CatCommand()

    @pytest.fixture
    def setup_filesystem(self, fs):
        """Фикстура для настройки тестовой файловой системы"""
        # Создаем тестовые файлы с разным содержимым
        fs.create_file("/test/file1.txt", contents="Hello, World!\nThis is file1.")
        fs.create_file("/test/file2.txt", contents="Content of file2")
        fs.create_file("/test/empty.txt", contents="")

        # Создаем директории
        fs.create_dir("/test/directory")
        fs.create_dir("/test/empty_directory")

        return fs

    def test_command_name(self, command):
        """Тест имени команды"""
        assert command.name == "cat"

    def test_cat_file_successfully(self, command, setup_filesystem):
        """Тест: успешный вывод содержимого файла"""
        with patch('builtins.print') as mock_print:
            command.execute(["test/file1.txt"], [])

            # Проверяем, что содержимое файла было выведено
            mock_print.assert_called_once_with("Hello, World!\nThis is file1.")

    def test_cat_empty_file(self, command, setup_filesystem):
        """Тест: вывод пустого файла"""
        with patch('builtins.print') as mock_print:
            command.execute(["/test/empty.txt"], [])

            # Проверяем, что была выведена пустая строка
            mock_print.assert_called_once_with("")


    def test_cat_nonexistent_file_raises_error(self, command, setup_filesystem):
        """Тест: вывод несуществующего файла вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            command.execute(["nonexistent.txt"], [])

    def test_cat_directory_raises_error(self, command, setup_filesystem):
        """Тест: вывод директории вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError, match=f"{command.name}: not a file: directory"):
            command.execute(["/test/directory"], [])

    def test_cat_no_arguments_uses_current_directory(self, command, setup_filesystem):
        """Тест: вызов без аргументов"""
        with pytest.raises(SyntaxError):
            command.execute([], [])
