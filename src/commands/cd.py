import os
from pathlib import Path
from .base import BaseCommand


class CdCommand(BaseCommand):
    @property
    def name(self):
        return "cd"

    def execute(self, args, options):
        if len(args) > 1:
            raise SyntaxError("Given more arguments than required")
        if not args or args[0] == '~':
            os.chdir(Path.home())
        else:
            path = Path(args[0])
            if path.exists():
                if not path.is_file():
                    os.chdir(path)
                else:
                    raise NotADirectoryError(f"Not a directory: {str(path).split('/')[-1]}")
            else:
                raise FileNotFoundError(f"No such file or directory: {str(path).split('/')[-1]}")
