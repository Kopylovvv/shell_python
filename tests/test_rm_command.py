import pytest
from pathlib import Path
from unittest.mock import patch

from commands.rm import RmCommand


class TestRmCommand:
    """Тесты для команды rm"""

    @pytest.fixture
    def command(self):
        """Фикстура для создания экземпляра команды"""
        return RmCommand(".trash")

    @pytest.fixture
    def setup_filesystem(self, fs):
        fs.create_dir("test")
        fs.create_file("test/file1.txt")
        fs.create_file("test/file2.txt")
        fs.create_dir("test/dir1")
        fs.create_file("test/dir1/subfile.txt")
        fs.create_dir("test/empty_dir")
        fs.create_dir(".trash")

        return fs

    def test_command_name(self, command):
        """Тест имени команды"""
        assert command.name == "rm"

    def test_no_arguments_raises_error(self, command):
        """Тест: вызов без аргументов вызывает SyntaxError"""
        with pytest.raises(SyntaxError):
            command.execute([], [])

    def test_too_many_arguments_raises_error(self, command):
        """Тест: слишком много аргументов вызывает SyntaxError"""
        with pytest.raises(SyntaxError):
            command.execute(["file1", "file2"], [])

    def test_delete_nonexistent_file_raises_error(self, command, setup_filesystem):
        """Тест: удаление несуществующего файла вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            command.execute(["nonexistent.txt"], [])

    def test_delete_directory_without_recursive_raises_error(self, command, setup_filesystem):
        """Тест: удаление директории без флага -r вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            command.execute(["dir1"], [])


    @patch('builtins.input', return_value='n')
    def test_delete_directory_recursively_without_confirmation(self, mock_input, command, setup_filesystem):
        """Тест: рекурсивное удаление директории без подтверждения (отмена)"""
        test_dir = Path("test/dir1")

        # Проверяем, что директория существует до попытки удаления
        assert test_dir.exists()

        # Пытаемся удалить директорию рекурсивно (отменяем)
        command.execute(["test/dir1"], ['r'])

        # Проверяем, что директория осталась на месте
        assert test_dir.exists()
        assert (test_dir / "subfile.txt").exists()



    @patch('builtins.input', return_value='invalid')
    def test_delete_directory_recursively_with_invalid_confirmation(self, mock_input, command, setup_filesystem):
        """Тест: рекурсивное удаление с невалидным подтверждением"""
        test_dir = Path("test/dir1")

        assert test_dir.exists()

        command.execute(["test/dir1"], ['r'])

        # Проверяем, что директория осталась на месте при невалидном ответе
        assert test_dir.exists()

    @patch('builtins.input', return_value='y')
    def test_delete_directory_recursively_with_confirmation(self, mock_input, command, setup_filesystem):
        """Тест: рекурсивное удаление директории с подтверждением"""

        test_dir = Path("test/dir1")

        # Проверяем, что директория существует до удаления
        assert test_dir.exists()
        assert (test_dir / "subfile.txt").exists()

        # Удаляем директорию рекурсивно
        command.execute(["test/dir1"], ['r'])

        # Проверяем, что директория перемещена в корзину
        assert not test_dir.exists()
        assert Path(".trash/dir1").exists()
        assert Path(".trash/dir1/subfile.txt").exists()


    def test_delete_file_successfully(self, command, setup_filesystem):
        """Тест: успешное удаление файла"""

        test_file = Path("test/file1.txt")

        # Проверяем, что файл существует до удаления
        assert test_file.exists()

        # Удаляем файл
        command.execute(["/test/file1.txt"], [])

        # Проверяем, что файл перемещен в корзину
        assert not test_file.exists()
        assert Path(".trash/file1.txt").exists()
