import sys
from .base import BaseCommand

class PwdCommand(BaseCommand):
    """
    команда для выхода из из программы
    """
    @property
    def name(self):
        return "exit"

    def execute(self, args, options):
        raise SystemExit()
