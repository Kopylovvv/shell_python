import shutil
from pathlib import Path

from .base import BaseCommand


class MvCommand(BaseCommand):
    """
    команда для перемещения файлов и директорий
    """
    @property
    def name(self):
        return "mv"

    def execute(self, args, options):
        if len(args) > 2:
            raise SyntaxError(f"{self.name}: given more arguments than required")
        elif len(args) < 2:
            raise SyntaxError(f"{self.name}: given less arguments than required")
        else:
            src = Path(args[0])
            dst = Path(args[1])
            if src.exists():
                if dst.exists():
                    shutil.move(src, dst)
                else:
                    raise FileNotFoundError(f"{self.name}: no such file or directory: {str(dst).split('/')[-1]}")
            else:
                raise FileNotFoundError(f"{self.name}: no such file or directory: {str(src).split('/')[-1]}")
