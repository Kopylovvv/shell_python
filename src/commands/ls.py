import os, stat, datetime
from pathlib import Path
from .base import BaseCommand
from src.utils.format_output import format_table


class LsCommand(BaseCommand):
    @property
    def name(self):
        return "ls"

    def execute(self, args, options):
        if len(args) > 1:
            raise SyntaxError("Given more arguments than required")
        if args:
            path = Path(args[0])
        else:
            path = Path('.')
        if path.exists():
            if not path.is_file():
                if 'l' in options:
                    output_list = [['File name', 'File size', 'Last change time', 'Permissions'], ]
                    for name in os.listdir(Path(path)):  # имя размер дата_изменения права_доступа
                        file_path = Path(path, name)
                        file_size = os.path.getsize(file_path)
                        change_timestamp = os.path.getmtime(file_path)
                        file_change_time = datetime.datetime.fromtimestamp(change_timestamp).strftime('%d.%m.%y %H:%M')
                        permissions = stat.filemode(Path.stat(file_path).st_mode)
                        output_list.append([name, file_size, file_change_time, permissions])
                    print(format_table(output_list))

                else:
                    print('\n'.join(os.listdir(path)))
            else:
                raise NotADirectoryError(f"Not a directory: {str(path).split('/')[-1]}")
        else:
            raise FileNotFoundError(f"No such file or directory: {str(path).split('/')[-1]}")
