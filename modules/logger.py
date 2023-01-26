# Based on https://gist.github.com/Willy-JL/3eaa171144b3bb0a4602c7b537f90036
import sys
from contextlib import contextmanager

# Backup original functionality
_stdout = sys.stdout
_stderr = sys.stderr
_stdin = sys.stdin

# Used to temporarily stop output to log file
_pause_file_output = False


def _file_write(message):
    if _pause_file_output:
        return
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(message)


class __stdout_override:
    def write(self, message):
        _stdout.write(message)
        _file_write(message)

    def __getattr__(self, name):
        return getattr(_stdout, name)


class __stderr_override:
    def write(self, message):
        _stderr.write(message)
        _file_write(message)

    def __getattr__(self, name):
        return getattr(_stderr, name)


class __stdin_override:
    def readline(self):
        message = _stdin.readline()
        _file_write(message)
        return message

    def __getattr__(self, name):
        # The input() function tries to use sys.stdin.fileno()
        # and then do the printing and input reading on the C
        # side, causing this .readline() override to not work.
        # Denying access to .fileno() fixes this and forces
        # input() to use sys.stdin.readline()
        if name == "fileno":
            raise AttributeError
        return getattr(_stdin, name)


@contextmanager
def pause_file_output():
    global _pause_file_output
    _pause_file_output = True
    yield
    _pause_file_output = False


pause = pause_file_output


# Create / clear log file
open("log.txt", "w").close()

# Apply overrides
sys.stdout = __stdout_override()
sys.stderr = __stderr_override()
sys.stdin = __stdin_override()