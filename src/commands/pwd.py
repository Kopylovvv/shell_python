from pathlib import Path
from .base import BaseCommand

class PwdCommand(BaseCommand):
    @property
    def name(self):
        return "pwd"

    def execute(self, args, options):
        print(Path.cwd())