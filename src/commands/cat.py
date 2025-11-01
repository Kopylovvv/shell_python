from pathlib import Path
import os
from .base import BaseCommand

class CatCommand(BaseCommand):
    """
    команда для вывода содержимого файлов
    """
    @property
    def name(self):
        return "cat"

    def execute(self, args, options):
        if args:
            path = Path(args[0])
        else:
            raise SyntaxError(f"{self.name}: no arguments given")
        if path.exists():
            if os.access(path, os.R_OK):
                if path.is_file():
                    with open(path) as file:
                        print(file.read())
                else:
                    raise FileNotFoundError(f"{self.name}: not a file: {str(path).split('/')[-1]}")
            else:
                raise PermissionError(f"{self.name}: access denied")
        else:
            raise FileNotFoundError(f"{self.name}: no such file or directory: {str(path).split('/')[-1]}")

