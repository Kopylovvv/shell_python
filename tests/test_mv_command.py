import pytest
from pathlib import Path
from unittest.mock import Mock

from commands.mv import MvCommand


class TestMvCommand:
    """Тесты для команды mv"""

    @pytest.fixture
    def mv_command(self):
        """Фикстура для создания экземпляра команды"""
        return MvCommand()

    @pytest.fixture
    def setup_filesystem(self, fs):
        return fs

    def test_command_name(self, mv_command):
        """Тест имени команды"""
        assert mv_command.name == "mv"

    def test_mv_command_with_too_many_args(self, mv_command, setup_filesystem):
        """Тест: слишком много аргументов вызывает SyntaxError"""

        with pytest.raises(SyntaxError) as exc_info:
            mv_command.execute(["file1", "file2", "file3"], [])

        assert "given more arguments than required" in str(exc_info.value)

    def test_mv_command_with_too_few_args(self, mv_command, setup_filesystem):
        """Тест: слишком мало аргументов вызывает SyntaxError"""
        with pytest.raises(SyntaxError) as exc_info:
            mv_command.execute(["file1"], [])

        assert "given less arguments than required" in str(exc_info.value)

    def test_mv_command_source_not_exists(self, mv_command, setup_filesystem):
        """Тест: исходный файл не существует вызывает FileNotFoundError"""
        fs = setup_filesystem
        fs.create_file("existing_file.txt")

        with pytest.raises(FileNotFoundError) as exc_info:
            mv_command.execute(["nonexistent.txt", "existing_file.txt"], [])

    def test_mv_command_destination_not_exists(self, mv_command, setup_filesystem):
        """Тест: целевая директория не существует вызывает FileNotFoundError"""
        fs = setup_filesystem
        fs.create_file("source.txt")

        with pytest.raises(FileNotFoundError) as exc_info:
            mv_command.execute(["source.txt", "nonexistent_dir/target.txt"], [])


    def test_mv_file_successfully(self, mv_command, setup_filesystem):
        """Тест: успешное перемещение файла"""
        fs = setup_filesystem
        fs.create_file("source.txt")
        fs.create_dir("target_dir")

        mv_command.execute(["source.txt", "target_dir"], [])

        # Проверяем, что файл перемещен
        assert not Path("source.txt").exists()
        assert Path("target_dir/source.txt").exists()

    def test_mv_directory_successfully(self, mv_command, setup_filesystem):
        """Тест: успешное перемещение директории"""
        fs = setup_filesystem
        fs.create_dir("source_dir")
        fs.create_file("source_dir/file1.txt")
        fs.create_file("source_dir/file2.txt")
        fs.create_dir("target_parent")

        mv_command.execute(["source_dir", "target_parent"], [])

        # Проверяем, что директория перемещена со всем содержимым
        assert not Path("source_dir").exists()
        assert Path("target_parent/source_dir").exists()
        assert Path("target_parent/source_dir/file1.txt").exists()
        assert Path("target_parent/source_dir/file2.txt").exists()


    def test_mv_to_non_writable_directory(self, mv_command, setup_filesystem):
        """Тест: попытка перемещения в недоступную для записи директорию"""
        fs = setup_filesystem
        if hasattr(fs, 'add_restrictions'):  # Проверяем поддержку ограничений в pyfakefs
            fs.create_file("source.txt")
            fs.create_dir("readonly_dir")

            fs.chmod("readonly_dir", 0o444)

            with pytest.raises(PermissionError):
                mv_command.execute(["source.txt", "readonly_dir"], [])
