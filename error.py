# Arcyou's error library. Handles any errors that may be thrown in the process
# of interpreting an Arcyou program.

# Copyright 2015 Benjamin Kulas
#
# This file is part of Arcyóu.
#
# Arcyóu is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Arcyóu is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Arcyóu.  If not, see <http://www.gnu.org/licenses/>.

from sys import exit

ERRORS = {'strmax': "Too many string literals are in the program. The maximum is 65536.",
          'missing-)': "A closing parenthesis is missing from the program.",
          'missing-(': "An opening parenthesis is missing from the program.",
          'badtype': "A function received arguments of the wrong type.",
          'missing-"': "A double-quoted string (\"...\") was not ended correctly.",
          'expected-function': "A cons cell was not begun with a function.",
          'value': "A function did not receive the right type of arguments.",
          'arguments': "A function did not receive the right number of arguments."}

class ArcError:
    def __init__(self, shortmsg):
        print(''.join(["Error: ", shortmsg, '\n', ERRORS[shortmsg]]))
        exit(1)
