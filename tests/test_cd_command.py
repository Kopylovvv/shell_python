import pytest
from pathlib import Path
import os
from unittest.mock import patch

from commands.cd import CdCommand


class TestCdCommand:
    """Тесты для команды cd"""

    @pytest.fixture
    def command(self):
        """Фикстура для создания экземпляра команды"""
        return CdCommand()

    @pytest.fixture
    def setup_filesystem(self, fs):
        """Фикстура для настройки тестовой файловой системы"""
        # Создаем тестовую структуру директорий
        fs.create_dir("/home/user")
        fs.create_dir("/home/user/documents")
        fs.create_dir("/home/user/documents/projects")
        fs.create_dir("/home/user/empty_dir")

        # Создаем файл (не директорию)
        fs.create_file("/home/user/file.txt")

        # Устанавливаем домашнюю директорию
        fs.create_dir("/home/test_user")
        fs.add_mount_point('/home/test_user', '/home/test_user')

        return fs

    def test_command_name(self, command):
        """Тест имени команды"""
        assert command.name == "cd"

    def test_cd_to_directory_successfully(self, command, setup_filesystem):
        """Тест: успешное изменение директории"""
        # Начинаем с корневой директории
        original_cwd = Path.cwd()

        try:
            # Меняем директорию
            command.execute(["/home/user/documents"], [])

            # Проверяем, что директория изменилась
            assert Path.cwd() == Path("/home/user/documents")
        finally:
            # Возвращаемся обратно
            os.chdir(original_cwd)

    def test_cd_to_nested_directory(self, command, setup_filesystem):
        """Тест: переход во вложенную директорию"""
        original_cwd = Path.cwd()

        try:
            # Переходим в глубоко вложенную директорию
            command.execute(["/home/user/documents/projects"], [])

            # Проверяем, что директория изменилась
            assert Path.cwd() == Path("/home/user/documents/projects")
        finally:
            os.chdir(original_cwd)

    def test_cd_home_with_tilde(self, command, setup_filesystem):
        """Тест: переход в домашнюю директорию с помощью ~"""
        original_cwd = Path.cwd()

        try:
            # Мокаем Path.home чтобы вернуть предсказуемый путь
            with patch.object(Path, 'home', return_value=Path("/home/test_user")):
                command.execute(["~"], [])

                # Проверяем, что перешли в домашнюю директорию
                assert Path.cwd() == Path("/home/test_user")
        finally:
            os.chdir(original_cwd)

    def test_cd_home_no_arguments(self, command, setup_filesystem):
        """Тест: переход в домашнюю директорию без аргументов"""
        original_cwd = Path.cwd()

        try:
            # Мокаем Path.home чтобы вернуть предсказуемый путь
            with patch.object(Path, 'home', return_value=Path("/home/test_user")):
                command.execute([], [])

                # Проверяем, что перешли в домашнюю директорию
                assert Path.cwd() == Path("/home/test_user")
        finally:
            os.chdir(original_cwd)

    def test_cd_to_nonexistent_directory_raises_error(self, command, setup_filesystem):
        """Тест: переход в несуществующую директорию вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError, match=f"{command.name}: no such file or directory: nonexistent_dir"):
            command.execute(["nonexistent_dir"], [])

    def test_cd_to_file_raises_error(self, command, setup_filesystem):
        """Тест: попытка перейти в файл вызывает NotADirectoryError"""
        with pytest.raises(NotADirectoryError, match=f"{command.name}: not a directory: file.txt"):
            command.execute(["/home/user/file.txt"], [])

    def test_cd_with_multiple_arguments_raises_error(self, command, setup_filesystem):
        """Тест: несколько аргументов вызывают SyntaxError"""
        with pytest.raises(SyntaxError, match=f"{command.name}: given more arguments than required"):
            command.execute(["/home/user", "/home/user/documents"], [])

    def test_cd_to_relative_path(self, command, setup_filesystem):
        """Тест: переход по относительному пути"""
        original_cwd = Path.cwd()

        try:
            # Переходим в начальную директорию
            os.chdir("/home/user")

            # Переходим в documents по относительному пути
            command.execute(["documents"], [])

            # Проверяем, что директория изменилась
            assert Path.cwd() == Path("/home/user/documents")
        finally:
            os.chdir(original_cwd)

    def test_cd_to_parent_directory(self, command, setup_filesystem):
        """Тест: переход в родительскую директорию"""
        original_cwd = Path.cwd()

        try:
            # Начинаем с вложенной директории
            os.chdir("/home/user/documents/projects")

            # Переходим на уровень выше
            command.execute([".."], [])

            # Проверяем, что директория изменилась
            assert Path.cwd() == Path("/home/user/documents")
        finally:
            os.chdir(original_cwd)

    def test_cd_to_current_directory(self, command, setup_filesystem):
        """Тест: переход в текущую директорию (.)"""
        original_cwd = Path.cwd()

        try:
            # Начинаем с определенной директории
            os.chdir("/home/user/documents")

            # "Переходим" в текущую директорию
            command.execute(["."], [])

            # Проверяем, что остались в той же директории
            assert Path.cwd() == Path("/home/user/documents")
        finally:
            os.chdir(original_cwd)

    def test_cd_to_empty_directory(self, command, setup_filesystem):
        """Тест: переход в пустую директорию"""
        original_cwd = Path.cwd()

        try:
            command.execute(["/home/user/empty_dir"], [])

            # Проверяем, что перешли в пустую директорию
            assert Path.cwd() == Path("/home/user/empty_dir")
            assert len(list(Path.cwd().iterdir())) == 0  # Директория пуста
        finally:
            os.chdir(original_cwd)

    def test_cd_with_special_characters_in_path(self, command, setup_filesystem):
        """Тест: переход в директорию со специальными символами в имени"""
        # Создаем директорию со специальными символами
        fs = setup_filesystem
        fs.create_dir("/home/user/my-dir")
        fs.create_dir("/home/user/dir with spaces")

        original_cwd = Path.cwd()

        try:
            # Тестируем директорию с дефисом
            command.execute(["/home/user/my-dir"], [])
            assert Path.cwd() == Path("/home/user/my-dir")

            # Тестируем директорию с пробелами
            os.chdir("/home/user")
            command.execute(["dir with spaces"], [])
            assert Path.cwd() == Path("/home/user/dir with spaces")
        finally:
            os.chdir(original_cwd)

    def test_error_message_format_nonexistent(self, command, setup_filesystem):
        """Тест: формат сообщения об ошибке для несуществующей директории"""
        with pytest.raises(FileNotFoundError) as exc_info:
            command.execute(["/nonexistent/path"], [])
        assert f"{command.name}: no such file or directory: path" in str(exc_info.value)

    def test_error_message_format_not_a_directory(self, command, setup_filesystem):
        """Тест: формат сообщения об ошибке для файла"""
        with pytest.raises(NotADirectoryError) as exc_info:
            command.execute(["/home/user/file.txt"], [])
        assert f"{command.name}: not a directory: file.txt" in str(exc_info.value)

    def test_cd_preserves_environment(self, command, setup_filesystem):
        """Тест: команда cd не влияет на другие переменные окружения"""
        original_cwd = Path.cwd()
        original_env = os.environ.copy()

        try:
            # Выполняем команду cd
            command.execute(["/home/user/documents"], [])

            # Проверяем, что текущая директория изменилась
            assert Path.cwd() == Path("/home/user/documents")

            # Проверяем, что переменные окружения не изменились
            assert os.environ == original_env

        finally:
            os.chdir(original_cwd)