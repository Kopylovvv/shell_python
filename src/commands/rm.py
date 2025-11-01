import shutil
from pathlib import Path

from .base import BaseCommand

class RmCommand(BaseCommand):
    """
    команда для удаления файлов и директорий

    перемещает файлы в корзину (.trash) вместо удаления
    поддерживает рекурсивное удаление директорий
    """

    def __init__(self, trash_dir_path: str | Path = Path(__file__).parent.parent.parent / ".trash"):
        self._trash_dir_path = trash_dir_path

    @property
    def name(self):
        return "rm"

    def execute(self, args, options):
        if len(args) > 1:
            raise SyntaxError(f"{self.name}: given more arguments than required")
        elif len(args) < 1:
            raise SyntaxError(f"{self.name}: given less arguments than required")
        else:
            src = Path(args[0])
            dst = self._trash_dir_path
            if 'r' in options:
                if src.exists():
                    answer = input(f"{self.name}: are you sure you want to delete {src.name}: [Y/N]: ").lower()
                    if answer == 'y':
                        shutil.move(src, dst)
                else:
                    raise FileNotFoundError(f"{self.name}: no such file or directory: {str(src).split('/')[-1]}")
            else:
                if src.exists() and src.is_file():
                    shutil.move(src, dst)
                else:
                    raise FileNotFoundError(f"{self.name}: {str(src).split('/')[-1]}: is a directory")
