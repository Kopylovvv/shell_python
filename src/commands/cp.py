import shutil
from pathlib import Path
from .base import BaseCommand

class CpCommand(BaseCommand):
    """
    команда для копирования файлов или директорий

    поддерживает рекурсивное копирование директорий
    """
    @property
    def name(self):
        return "cp"

    def execute(self, args, options):
        if len(args) > 2:
            raise SyntaxError(f"{self.name}: given more arguments than required")
        elif len(args) < 2:
            raise SyntaxError(f"{self.name}: given less arguments than required")
        else:
            src = Path(args[0])
            dst = Path(args[1])
            if 'r' in options:
                if src.exists():
                    shutil.copytree(src, dst / src.name, dirs_exist_ok=True)
                else:
                    raise FileNotFoundError(f"{self.name}: no such file or directory: {str(src).split('/')[-1]}")
            else:
                if src.exists() and src.is_file():
                    shutil.copy2(src, dst)
                else:
                    raise FileNotFoundError(f"{self.name}: {str(src).split('/')[-1]}: is a directory")
