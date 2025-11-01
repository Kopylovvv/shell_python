import pytest
from pathlib import Path

from commands.cp import CpCommand


class TestCpCommand:
    """Тесты для команды cp"""

    @pytest.fixture
    def command(self):
        """Фикстура для создания экземпляра команды"""
        return CpCommand()

    @pytest.fixture
    def setup_filesystem(self, fs):
        """Фикстура для настройки тестовой файловой системы"""
        # Создаем базовую структуру файлов и директорий
        fs.create_dir("source")
        fs.create_dir("target")

        # Создаем тестовые файлы
        fs.create_file("source/file1.txt", contents="content1")
        fs.create_file("source/file2.txt", contents="content2")

        # Создаем структуру директорий для рекурсивного копирования
        fs.create_dir("source/dir1")
        fs.create_file("source/dir1/subfile1.txt", contents="subcontent1")
        fs.create_file("source/dir1/subfile2.txt", contents="subfile2 content")
        fs.create_dir("source/dir1/subdir")
        fs.create_file("source/dir1/subdir/deepfile.txt", contents="deep content")

        return fs

    def test_command_name(self, command):
        """Тест имени команды"""
        assert command.name == "cp"

    def test_one_argument_raises_error(self, command):
        """Тест: только один аргумент вызывает SyntaxError"""
        with pytest.raises(SyntaxError):
            command.execute(["source.txt"], [])

    def test_three_arguments_raises_error(self, command):
        """Тест: три аргумента вызывают SyntaxError"""
        with pytest.raises(SyntaxError):
            command.execute(["src.txt", "dst.txt", "extra.txt"], [])

    def test_copy_nonexistent_file_raises_error(self, command, setup_filesystem):
        """Тест: копирование несуществующего файла вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            command.execute(["nonexistent.txt", "/target"], [])

    def test_copy_directory_without_recursive_raises_error(self, command, setup_filesystem):
        """Тест: копирование директории без флага -r вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            command.execute(["/source/dir1", "/target"], [])

    def test_copy_file_successfully(self, command, setup_filesystem):
        """Тест: успешное копирование файла"""
        source_file = Path("/source/file1.txt")
        target_dir = Path("/target")

        # Проверяем, что исходный файл существует, а целевого еще нет
        assert source_file.exists()
        assert not (target_dir / "file1.txt").exists()

        # Копируем файл
        command.execute(["/source/file1.txt", "/target"], [])

        # Проверяем, что файл скопирован
        assert source_file.exists()  # исходный должен остаться
        assert (target_dir / "file1.txt").exists()
        assert (target_dir / "file1.txt").read_text() == "content1"


    def test_copy_directory_recursively(self, command, setup_filesystem):
        """Тест: рекурсивное копирование директории"""
        source_dir = Path("source/dir1")
        target_dir = Path("target")

        assert source_dir.exists()
        assert (source_dir / "subfile1.txt").exists()
        assert (source_dir / "subdir").exists()

        # Копируем директорию рекурсивно
        command.execute(["source/dir1", "target"], ['r'])

        # Проверяем, что вся структура скопирована
        assert source_dir.exists()  # исходная должна остаться
        assert (target_dir / "dir1").exists()
        assert (target_dir / "dir1" / "subfile1.txt").exists()
        assert (target_dir / "dir1" / "subfile2.txt").exists()
        assert (target_dir / "dir1" / "subdir").exists()
        assert (target_dir / "dir1" / "subdir" / "deepfile.txt").exists()

        # Проверяем содержимое файлов
        assert (target_dir / "dir1" / "subfile1.txt").read_text() == "subcontent1"
        assert (target_dir / "dir1" / "subdir" / "deepfile.txt").read_text() == "deep content"


    def test_error_message_format_nonexistent(self, command, setup_filesystem):
        """Тест: формат сообщения об ошибке для несуществующего файла"""
        with pytest.raises(FileNotFoundError):
            command.execute(["nonexistent", "target"], [])


    def test_error_message_format_directory_without_r(self, command, setup_filesystem):
        """Тест: формат сообщения об ошибке для директории без -r"""
        with pytest.raises(FileNotFoundError):
            command.execute(["source/dir1", "target"], [])


