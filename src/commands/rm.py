import shutil
from pathlib import Path
from .base import BaseCommand

class RmCommand(BaseCommand):
    @property
    def name(self):
        return "rm"

    def execute(self, args, options):
        if len(args) > 1:
            raise SyntaxError("Given more arguments than required")
        elif len(args) < 1:
            raise SyntaxError("Given less arguments than required")
        else:
            src = Path(args[0])
            dst = Path(__file__).parent.parent / ".trash"
            if 'r' in options:
                if src.exists():
                    shutil.move(src, dst)
                else:
                    raise FileNotFoundError(f"No such file or directory: {str(src).split('/')[-1]}")
            else:
                if src.exists() and src.is_file():
                    shutil.move(src, dst)
                else:
                    raise FileNotFoundError(f"{str(src).split('/')[-1]}: is a directory")
