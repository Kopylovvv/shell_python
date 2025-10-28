import os
from pathlib import Path
from .base import BaseCommand


class CdCommand(BaseCommand):
    @property
    def name(self):
        return "cd"

    def execute(self, args, options):
        path = Path(args)
        if not args or args == '~':
            os.chdir(Path.home())
        else:
            if path.exists():
                if not path.is_file():
                    os.chdir(path)
                else:
                    raise NotADirectoryError(f"Not a directory: {str(path).split('/')[-1]}")
            else:
                raise FileNotFoundError(f"No such file or directory: {str(path).split('/')[-1]}")
