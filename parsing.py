# Arcyou's parsing library. Handles comment removal, string literals, omitted
# close-parens, and abstract syntax tree creation.

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

from error import ArcError
from re import sub, MULTILINE
from sys import getrecursionlimit, setrecursionlimit

ESCAPES = {'n': '\n',
           't': '\t',
           'v': '\v',
           'a': '\a',
           'b': '\b',
           'f': '\f',
           'r': '\r'}

def parse(code):
    """
The top-level function for this library, the only one that should be called
externally. It applies all of the below functions in sequence to some raw
code that it is passed.
    """
    old_rl = getrecursionlimit()
    setrecursionlimit(code.count('(') + 50) # This should be comfortable
    stage1 = remove_comments(code)
    stage2, literals = extract_string_literals(stage1)
    stage3 = add_close_parens(stage2)
    stage4 = tokenize(stage3)
    stage5 = clean(stage4)
    stage6 = convints(stage5)
    stage7 = insert_string_literals(stage6, literals)
    setrecursionlimit(old_rl)
    return stage7

def remove_comments(code):
    """
Remove all comments from a program.
    """
    no_comments = sub(r";.*$", '', code, flags=MULTILINE)
    return sub(r" {2,}", ' ', no_comments.replace('\n', ' '))

def extract_string_literals(code):
    """
Deal with string literals inside an Arcyou program. Also handles Unicode
escapes, ASCII escapes, and a few other standard ones.
    """
    code = code.replace('\x02', '')
    final = ""
    in_string = False
    literals = []
    pointer = 0
    index = 0
    temp = ""
    while pointer < len(code):
        char = code[pointer]
        if in_string:
            if char == '\\':
                if code[pointer+1] == 'u':
                    # Handle Unicode escapes
                    temp += chr(int(code[pointer+2:pointer+6], 16))
                    pointer += 5
                elif code[pointer+1] == 'x':
                    # Handle \x.. escapes
                    temp += chr(int(code[pointer+2:pointer+4], 16))
                    pointer += 3
                else:
                    # Handle all other escapes
                    if code[pointer+1] in ESCAPES:
                        temp += ESCAPES[code[pointer+1]]
                    else:
                        temp += code[pointer+1]
                    pointer += 1
            elif char == '\"':
                if temp in literals:
                        final += ' \x02' + chr(literals.index(temp)) + ' '
                else:
                    literals.append(temp)
                    if index <= 0xFFFF:
                        final += '\x02' + chr(index)
                    else:
                        errors.ArcError('strmax')
                    index += 1
                    temp = ""
                in_string = False

            else:
                temp += char
        else:
            if char == '\"':
                in_string = True
            else:
                final += char
        pointer += 1
    if in_string:
        ArcError('missing-"')
    return final, literals

def add_close_parens(code):
    """
This is a feature which allows one to strip a fair amount of bytes off their
program. Any closing parentheses at the end of the program can be omitted. This
function adds them back in for parsing purposes.
    """
    return code + ')' * (code.count('(')-code.count(')'))

def tokenize(code):
    """
Split the code into indiviual-character tokens in a nested list.
 Example:
"(eq (+ x 1) y)" -> ['e','q',' ', ['+',' ','x',' ','1'],' ','y']
    """
    def parsehelper(level=0):
        try:
            token = next(tokens)
        except StopIteration:
            if level != 0:
                errors.ArcError("missing-)")
            else:
                return []
        if token == ')':
            if level == 0:
                errors.ArcError("missing-(")
            else:
                return []
        elif token == '(':
            return [parsehelper(level+1)] + parsehelper(level)
        else:
            return [token] + parsehelper(level)
    tokens = iter(code)
    return parsehelper()

def clean(icode):
    """
Clean up the output from tokenize(). Also converts numeric literals.
Example:
tokenize("(eq (+ x 1) y)") -> ['eq',('+','x',1),'y']
    """
    code = icode[:]
    i = 0
    temp = ""
    while i< len(code):
        item = code[i]
        if isinstance(item, str):
            if item == ' ':
                if temp != "":
                    code[i] = temp
                    temp = ""
                else:
                    code.pop(i)
                    i -= 1
            else:
                temp += code.pop(i)
                i -= 1
        else: # it's a list
            if temp != "":
                code.insert(i, temp)
                temp = ""
                i += 1
            code[i] = clean(item[:])
        i += 1
    if temp != "":
        code.append(temp)
    return code

def convints(icode):
    """
Trawl the AST looking for valid numbers. If it finds any, it converts them.
    """
    code = []
    for item in icode:
        if isinstance(item, list):
            code.append(convints(item))
        elif is_valid_int(item):
            code.append(int(item))
        elif is_valid_float(item):
            code.append(float(item))
        else:
            code.append(item)
    return(code)

def insert_string_literals(icode, literals):
    """
Re-insert the string literals into the AST.
    """
    code = icode[:]
    i = 0
    while i < len(code):
        item = code[i]
        if isinstance(item, str) and item.startswith('\x02'):
            code[i] = '"' + literals[ord(item[1])] + '"'
        elif isinstance(item, list):
            code[i] = insert_string_literals(item, literals)
        i += 1
    return code

def is_valid_int(thing):
    try:
        int(thing)
        return True
    except ValueError:
        return False

def is_valid_float(thing):
    try:
        float(thing)
        return True
    except ValueError:
        return False
