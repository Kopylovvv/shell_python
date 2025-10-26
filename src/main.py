from src.core import ShellCore
import sys

def run():
    core = ShellCore()
    core.auto_discover_commands()
    for line in sys.stdin:
        core.execute_command(line)




if __name__ == "__main__":
    run()
