import pytest
from pathlib import Path
import os
import datetime
from unittest.mock import patch

from commands.ls import LsCommand


class TestLsCommand:
    """Тесты для команды ls"""

    @pytest.fixture
    def command(self):
        """Фикстура для создания экземпляра команды"""
        return LsCommand()

    @pytest.fixture
    def setup_filesystem(self, fs):
        """Фикстура для настройки тестовой файловой системы"""
        # Создаем тестовую структуру директорий и файлов
        fs.create_dir("/test/dir1")
        fs.create_dir("/test/empty_dir")
        fs.create_dir("/test/dir_with_many_files")

        # Создаем файлы с разными размерами и временем изменения
        fs.create_file("/test/file1.txt", contents="content1")
        fs.create_file("/test/file2.py", contents="content of file2")
        fs.create_file("/test/.hidden_file", contents="hidden content")

        # Создаем несколько файлов в директории
        fs.create_file("/test/dir_with_many_files/a.txt", contents="a")
        fs.create_file("/test/dir_with_many_files/b.txt", contents="bb")
        fs.create_file("/test/dir_with_many_files/c.txt", contents="ccc")

        # Создаем файл для тестирования (не директорию)
        fs.create_file("/test/regular_file.txt", contents="test content")

        return fs

    def test_command_name(self, command):
        """Тест имени команды"""
        assert command.name == "ls"

    def test_ls_no_arguments_current_directory(self, command, setup_filesystem):
        """Тест: вывод содержимого текущей директории без аргументов"""
        original_cwd = Path.cwd()

        try:
            # Переходим в тестовую директорию
            os.chdir("/test")

            with patch('builtins.print') as mock_print:
                command.execute([], [])

                # Проверяем, что были выведены все файлы и директории
                mock_print.assert_called_once()
                output = mock_print.call_args[0][0]
                assert "file1.txt" in output
                assert "file2.py" in output
                assert "dir1" in output
                assert "dir_with_many_files" in output
                # Скрытые файлы тоже должны отображаться
                assert ".hidden_file" in output
        finally:
            os.chdir(original_cwd)

    def test_ls_specific_directory(self, command, setup_filesystem):
        """Тест: вывод содержимого указанной директории"""
        with patch('builtins.print') as mock_print:
            command.execute(["/test/dir_with_many_files"], [])

            # Проверяем, что были выведены файлы из указанной директории
            mock_print.assert_called_once()
            output = mock_print.call_args[0][0]
            assert "a.txt" in output
            assert "b.txt" in output
            assert "c.txt" in output

    def test_ls_detailed_output(self, command, setup_filesystem):
        """Тест: подробный вывод с флагом -l"""
        with patch('builtins.print') as mock_print:
            command.execute(["/test"], ['l'])

            # Проверяем, что была вызвана format_table с правильными данными
            mock_print.assert_called_once()
            # Проверяем, что вывод содержит заголовки таблицы
            call_args = mock_print.call_args[0][0]
            assert "File name" in call_args
            assert "File size" in call_args
            assert "Last change time" in call_args
            assert "Permissions" in call_args

    def test_ls_empty_directory(self, command, setup_filesystem):
        """Тест: вывод пустой директории"""
        with patch('builtins.print') as mock_print:
            command.execute(["/test/empty_dir"], [])

            # Проверяем, что была выведена пустая строка
            mock_print.assert_called_once_with("")

    def test_ls_nonexistent_directory_raises_error(self, command, setup_filesystem):
        """Тест: вывод несуществующей директории вызывает FileNotFoundError"""
        with pytest.raises(FileNotFoundError, match=f"{command.name}: no such file or directory: nonexistent"):
            command.execute(["nonexistent"], [])

    def test_ls_file_instead_of_directory_raises_error(self, command, setup_filesystem):
        """Тест: вывод файла вместо директории вызывает NotADirectoryError"""
        with pytest.raises(NotADirectoryError, match=f"{command.name}: not a directory: regular_file.txt"):
            command.execute(["/test/regular_file.txt"], [])

    def test_ls_with_multiple_arguments_raises_error(self, command, setup_filesystem):
        """Тест: несколько аргументов вызывают SyntaxError"""
        with pytest.raises(SyntaxError, match=f"{command.name}: given more arguments than required"):
            command.execute(["/test", "/other"], [])


    def test_ls_relative_path(self, command, setup_filesystem):
        """Тест: вывод с относительным путем"""
        original_cwd = Path.cwd()

        try:
            # Переходим в родительскую директорию
            os.chdir("/")

            with patch('builtins.print') as mock_print:
                command.execute(["test"], [])

                # Проверяем, что были выведены файлы из относительного пути
                mock_print.assert_called_once()
                output = mock_print.call_args[0][0]
                assert "file1.txt" in output
                assert "dir1" in output
        finally:
            os.chdir(original_cwd)

    def test_ls_hidden_files_included(self, command, setup_filesystem):
        """Тест: скрытые файлы включаются в вывод"""
        with patch('builtins.print') as mock_print:
            command.execute(["/test"], [])

            # Проверяем, что скрытый файл присутствует в выводе
            mock_print.assert_called_once()
            output = mock_print.call_args[0][0]
            assert ".hidden_file" in output

    def test_ls_multiple_options_ignored_except_l(self, command, setup_filesystem):
        """Тест: дополнительные флаги кроме -l игнорируются"""
        with patch('builtins.print') as mock_print:
            command.execute(["/test"], ['a', 'l', 'h'])  # Флаги -a, -l, -h

            # Проверяем, что используется подробный вывод (из-за -l)
            mock_print.assert_called_once()
            # Должна быть вызвана format_table (признак подробного вывода)

    def test_ls_only_l_flag_matters(self, command, setup_filesystem):
        """Тест: только флаг -l влияет на формат вывода"""
        # Без флага -l
        with patch('builtins.print') as mock_print:
            command.execute(["/test"], ['a', 'h'])
            output_simple = mock_print.call_args[0][0]
            # Простой вывод - просто имена через перенос строки

        # С флагом -l
        with patch('builtins.print') as mock_print:
            command.execute(["/test"], ['l'])
            output_detailed = mock_print.call_args[0][0]
            # Подробный вывод - таблица



    def test_error_message_format_nonexistent(self, command, setup_filesystem):
        """Тест: формат сообщения об ошибке для несуществующей директории"""
        with pytest.raises(FileNotFoundError) as exc_info:
            command.execute(["/nonexistent/path"], [])
        assert f"{command.name}: no such file or directory: path" in str(exc_info.value)

    def test_error_message_format_not_a_directory(self, command, setup_filesystem):
        """Тест: формат сообщения об ошибке для файла"""
        with pytest.raises(NotADirectoryError) as exc_info:
            command.execute(["/test/regular_file.txt"], [])
        assert f"{command.name}: not a directory: regular_file.txt" in str(exc_info.value)

