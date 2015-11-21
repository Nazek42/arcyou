# Arcyou's error library. Handles any errors that may be thrown in the process
# of interpreting an Arcyou program.

from sys import exit

ERRORS = {'strmax': "Too many string literals are in the program. The maximum is 65536.",
          'missing-)': "A closing parenthesis is missing from the program.",
          'missing-(': "An opening parenthesis is missing from the program.",
          'badtype': "A function received arguments of the wrong type.",
          'missing-"': "A double-quoted string (\"...\") was not ended correctly.",
          'expected-function': "A cons cell was not begun with a function."}

class ArcError:
    def __init__(self, shortmsg):
        print(''.join(["Error: ", shortmsg, '\n', ERRORS[shortmsg]]))
        exit(1)
