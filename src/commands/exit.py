import sys
from .base import BaseCommand

class PwdCommand(BaseCommand):
    @property
    def name(self):
        return "exit"

    def execute(self, args, options):
        sys.exit(0)
