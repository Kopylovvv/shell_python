from pathlib import Path
import os
from .base import BaseCommand

class PwdCommand(BaseCommand):
    @property
    def name(self):
        return "cat"

    def execute(self, args, options):
        if args:
            path = Path(args)
        else:
            path = Path('.')
        if os.access(path, os.R_OK):
            if path.exists():
                if path.is_file():
                    with open(path) as file:
                        print(file.read())
                else:
                    raise FileNotFoundError(f"Not a file: {str(path).split('/')[-1]}")
            else:
                raise FileNotFoundError(f"No such file or directory: {str(path).split('/')[-1]}")
        else:
            raise PermissionError(f"Access denied")

