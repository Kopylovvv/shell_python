import os
from pathlib import Path
from .base import BaseCommand


class CdCommand(BaseCommand):
    @property
    def name(self):
        return "cd"

    def execute(self, args, options):
        file_path = Path(args)
        if not args or args == '~':
            os.chdir(Path.home())
        else:
            if file_path.exists():
                if not file_path.is_file():
                    os.chdir(args)
                else:
                    raise NotADirectoryError(f"Not a directory: {args.split('/')[-1]}")
            else:
                raise FileNotFoundError(f"No such file or directory: {args.split('/')[-1]}")
